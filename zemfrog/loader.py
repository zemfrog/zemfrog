import os
from glob import glob
from importlib import import_module
from typing import Dict, List


import pkg_resources
import click
from flask import Flask, Blueprint, send_from_directory
from flask.cli import load_dotenv, routes_command, run_command, shell_command
from flask_apispec import FlaskApiSpec
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from .exception import ZemfrogEnvironment
from .decorators import api_doc
from .helper import get_import_name, get_models, import_attr
from .repl import build_repl


def load_config(app: Flask):
    """
    Loads the configuration for your zemfrog application based on the environment
    ``ZEMFROG_ENV``, change your application environment in the file ``.flaskenv``.
    """

    path = os.path.join(app.root_path, ".flaskenv")
    load_dotenv(path)
    env = os.getenv("ZEMFROG_ENV")
    if not env:
        raise ZemfrogEnvironment("environment not found")

    import_name = get_import_name(app)
    app.config.from_object(import_name + "config." + env.capitalize())


def load_extensions(app: Flask):
    """
    The function to load all your flask extensions based on the ``EXTENSIONS`` configuration in config.py.
    """

    extensions = app.config.get("EXTENSIONS", [])
    import_name = get_import_name(app)
    for ext in extensions:
        ext = import_module(import_name + ext)
        init_func = getattr(ext, "init_app")
        init_func(app)


def load_staticfiles(app: Flask):
    """
    This function is to create multiple static files based on the ``STATICFILES`` configuration.
    """

    staticfiles = app.config.get("STATICFILES", [])
    for static in staticfiles:
        path, endpoint, static_folder = static
        static_host = None
        if len(static) == 4:
            static_host = static[-1]

        def serve_static(filename):
            cache_timeout = app.get_send_file_max_age(filename)
            return send_from_directory(
                static_folder, filename, cache_timeout=cache_timeout
            )

        app.add_url_rule(
            path.rstrip("/") + "/<path:filename>",
            endpoint=endpoint,
            host=static_host,
            view_func=serve_static,
        )


def load_models(app: Flask):
    """
    A function to load all your ORM models in the ``models`` directory.
    """

    app.models = {}
    true = app.config.get("CREATE_DB")
    import_name = get_import_name(app)
    if import_name:
        import_name = import_name.replace(".", "/")

    if true:
        models = [
            x.rsplit(".", 1)[0].replace(os.sep, ".")
            for x in glob(import_name + "models/**/*.py", recursive=True)
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
    import_name = get_import_name(app)
    for name in commands:
        try:
            n = import_name + name + ".command"
            cmd = import_attr(n)
        except ImportError:
            n = name + ".command"
            cmd = import_attr(n)

        app.cli.add_command(cmd)

    if import_name:
        for cmd in (run_command, shell_command, routes_command):
            app.cli.add_command(cmd)

        for ep in pkg_resources.iter_entry_points("flask.commands"):
            app.cli.add_command(ep.load(), ep.name)


def load_urls(app: Flask):
    """
    This function will load all urls in the main application.
    """

    import_name = get_import_name(app)
    routes = import_attr(import_name + "urls.routes")
    for url, view, methods in routes:
        app.add_url_rule(url, view_func=view, methods=methods)


def load_blueprints(app: Flask):
    """
    The function to load all blueprints based on the ``BLUEPRINTS`` configuration in config.py
    """

    blueprints = app.config.get("BLUEPRINTS", [])
    import_name = get_import_name(app)
    for name in blueprints:
        bp = import_name + name + ".routes.blueprint"
        bp: Blueprint = import_attr(bp)
        routes = import_name + name + ".urls.routes"
        routes = import_attr(routes)
        for url, view, methods in routes:
            bp.add_url_rule(url, view_func=view, methods=methods)

        app.register_blueprint(bp)


def load_middlewares(app: Flask):
    """
    Function to load all middlewares.
    """

    middlewares = app.config.get("MIDDLEWARES", [])
    import_name = get_import_name(app)
    for name in middlewares:
        name = import_name + name + ".init_middleware"
        middleware = import_attr(name)
        app.wsgi_app = middleware(app.wsgi_app)


def load_apis(app: Flask):
    """
    A function to load all of your API resources to flask based on the ``APIS`` configuration in config.py.
    """

    apis = app.config.get("APIS", [])
    import_name = get_import_name(app)
    api: Blueprint = import_attr(import_name + "api.api")
    for res in apis:
        res = import_module(import_name + res)
        endpoint = res.endpoint
        url_prefix = res.url_prefix
        routes = res.routes
        for detail in routes:
            route, view, methods = detail
            url = url_prefix + route
            e = endpoint + "_" + view.__name__
            api.add_url_rule(url, e, view_func=view, methods=methods)

    app.register_blueprint(api)


def load_error_handlers(app: Flask):
    """
    Function to load all error handlers
    """

    import_name = get_import_name(app)
    handlers = app.config.get("ERROR_HANDLERS", {})
    for code, view in handlers.items():
        view = import_attr(import_name + view + ".handler")
        app.register_error_handler(code, view)


def load_tasks(app: Flask):
    """
    Function to load all celery tasks based on ``TASKS`` configuration in config.py.
    """

    tasks = app.config.get("TASKS", [])
    import_name = get_import_name(app)
    for sv in tasks:
        import_module(import_name + sv)


def load_docs(app: Flask):
    """
    Function for creating api docs using ``flask-apispec``.
    """

    if not app.config.get("API_DOCS", False):
        return

    import_name = get_import_name(app)
    docs: FlaskApiSpec = import_attr(import_name + "extensions.apispec.docs")
    urls = import_module(import_name + "urls")
    docs_params = urls.docs
    routes = urls.routes
    for _, view, _ in routes:
        if docs_params:
            view = api_doc(**docs_params)(view)
        docs.register(view)

    apis = app.config.get("APIS", [])
    for res in apis:
        res = import_module(import_name + res)
        docs_params = res.docs
        routes = res.routes
        endpoint = res.endpoint
        for detail in routes:
            _, view, _ = detail
            e = endpoint + "_" + view.__name__
            if docs_params:
                view = api_doc(**docs_params)(view)
            docs.register(view, endpoint=e, blueprint="api")

    blueprints = app.config.get("BLUEPRINTS", [])
    for name in blueprints:
        bp = import_name + name + ".routes.blueprint"
        bp: Blueprint = import_attr(bp)
        urls = import_name + name + ".urls"
        urls = import_module(urls)
        docs_params = urls.docs
        routes = urls.routes
        for _, view, _ in routes:
            if docs_params:
                view = api_doc(**docs_params)(view)
            docs.register(view, blueprint=name)


def load_apps(app: Flask):
    """
    Load all applications and combine them together using ``DispatcherMiddleware``.
    """

    apps: List[Dict] = app.config.get("APPS", [])
    mounts = {}
    for a in apps:
        if not isinstance(a, dict):
            a = {"name": a}

        name = a["name"]
        path = a.get("path", "/" + name)
        help = a.get("help", "")
        yourapp: Flask = import_attr(name + ".wsgi.app")

        @click.command(name)
        def cli():
            build_repl(yourapp)

        cli.help = help
        app.cli.add_command(cli, name)
        mounts[path] = yourapp

    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, mounts)
