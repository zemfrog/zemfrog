import os
from flask import Flask
from os import getenv
from glob import glob
from importlib import import_module

from flask.cli import load_dotenv
from flask.blueprints import Blueprint
from flask_apispec import FlaskApiSpec, doc

from .generator import g_schema
from .exception import ZemfrogEnvironment
from .helper import get_models, import_attr


def load_config(app: Flask):
    """
    Loads the configuration for your zemfrog application based on the environment
    ``ZEMFROG_ENV``, change your application environment in the file ``.flaskenv``.
    """

    load_dotenv()
    env = getenv("ZEMFROG_ENV")
    if not env:
        raise ZemfrogEnvironment("environment not found")

    app.config.from_object("config." + env.capitalize())


def load_extensions(app: Flask):
    """
    The function to load all your flask extensions based on the ``EXTENSIONS`` configuration in config.py.
    """

    extensions = app.config.get("EXTENSIONS", [])
    for ext in extensions:
        ext = import_module(ext)
        init_func = getattr(ext, "init_app")
        init_func(app)


def load_models(app: Flask):
    """
    A function to load all your ORM models in the ``models`` directory.
    """

    app.models = {}
    true = app.config.get("CREATE_DB")
    if true:
        models = [
            x.rsplit(".", 1)[0].replace(os.sep, ".")
            for x in glob("models/**/*.py", recursive=True)
        ]
        for m in models:
            if "__init__" in m:
                m = m.replace(".__init__", "")
            mod = import_module(m)
            app.models[m] = get_models(mod)

        app.extensions["sqlalchemy"].db.create_all()


def load_commands(app: Flask):
    """
    A function to load all your commands and register them in the ``flask`` command.
    """

    commands = app.config.get("COMMANDS", [])
    for cmd in commands:
        cmd = cmd + ".command"
        cmd = import_attr(cmd)
        app.cli.add_command(cmd)


def load_blueprints(app: Flask):
    """
    The function to load all blueprints based on the ``BLUEPRINTS`` configuration in config.py
    """

    blueprints = app.config.get("BLUEPRINTS", [])
    for name in blueprints:
        bp = name + ".routes.blueprint"
        bp: Blueprint = import_attr(bp)
        routes = name + ".urls.routes"
        routes = import_attr(routes)
        for url, view, methods in routes:
            bp.add_url_rule(url, view_func=view, methods=methods)

        app.register_blueprint(bp)


def load_apis(app: Flask):
    """
    A function to load all of your API resources to flask based on the ``APIS`` configuration in config.py.
    """

    apis = app.config.get("APIS", [])
    api: Blueprint = import_attr("api.api")
    for res in apis:
        res = import_module(res)
        endpoint = res.endpoint
        url_prefix = res.url_prefix
        routes = res.routes
        for detail in routes:
            route, view, methods = detail
            url = url_prefix + route
            e = endpoint + "_" + view.__name__
            api.add_url_rule(url, e, view_func=view, methods=methods)

    app.register_blueprint(api)


def load_services(app: Flask):
    """
    Function to load all celery tasks based on ``SERVICES`` configuration in config.py.
    """

    services = app.config.get("SERVICES", [])
    for sv in services:
        import_module(sv)


def load_schemas(app: Flask):
    """
    A function to create marshmallow schema models automatically for all your ORM models.
    """

    for src, models in app.models.items():
        g_schema(src, models)


def load_docs(app: Flask):
    """
    Function for creating api docs using ``flask-apispec``.
    """

    if not app.config.get("API_DOCS", False):
        return

    docs: FlaskApiSpec = import_attr("extensions.apispec.docs")
    apis = app.config.get("APIS", [])
    for res in apis:
        res = import_module(res)
        api_docs = res.docs
        routes = res.routes
        endpoint = res.endpoint
        for detail in routes:
            _, view, _ = detail
            e = endpoint + "_" + view.__name__
            if api_docs:
                view = doc(**api_docs)(view)
            docs.register(view, endpoint=e, blueprint="api")

    blueprints = app.config.get("BLUEPRINTS", [])
    for name in blueprints:
        bp = name + ".routes.blueprint"
        bp: Blueprint = import_attr(bp)
        urls = name + ".urls"
        urls = import_module(urls)
        api_docs = urls.docs
        routes = urls.routes
        for _, view, _ in routes:
            if api_docs:
                view = doc(**api_docs)(view)
            docs.register(view, blueprint=name)
