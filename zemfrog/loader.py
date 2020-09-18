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
    Memuat konfigurasi untuk aplikasi zemfrog kamu dari environment
    ``ZEMFROG_ENV``, rubah environment aplikasi mu di file ``.flaskenv``.
    """

    load_dotenv()
    env = getenv("ZEMFROG_ENV")
    if not env:
        raise ZemfrogEnvironment("environment not found")

    app.config.from_object("config." + env.capitalize())


def load_extensions(app: Flask):
    """
    Fungsi untuk memuat semua ekstensi flask kamu.
    """

    extensions = app.config.get("EXTENSIONS", [])
    for ext in extensions:
        ext = import_module(ext)
        init_func = getattr(ext, "init_app")
        init_func(app)


def load_models(app: Flask):
    """
    Fungsi untuk memuat semua model ORM kamu.
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
    Fungsi untuk memuat semua command kamu dan mendaftarkan ke command ``flask``.
    """

    commands = app.config.get("COMMANDS", [])
    for cmd in commands:
        cmd = cmd + ".command"
        cmd = import_attr(cmd)
        app.cli.add_command(cmd)


def load_blueprints(app: Flask):
    """
    Fungsi untuk memuat semua blueprint flask yang sudah terdaftar di config ``BLUEPRINTS`` pada config.py
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
    Fungsi untuk memuat semua resource API kamu ke flask.
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
    Fungsi untuk memuat semua background task celery.
    """

    services = app.config.get("SERVICES", [])
    for sv in services:
        import_module(sv)


def load_schemas(app: Flask):
    """
    Fungsi untuk membuat model schema menggunakan marshmallow secara otomatis.
    """

    for src, models in app.models.items():
        g_schema(src, models)


def load_docs(app: Flask):
    """
    Fungsi untuk membuat api docs.
    """

    apis = app.config.get("APIS", [])
    docs: FlaskApiSpec = import_attr("extensions.apispec.docs")
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

    api_docs = app.config.get("API_DOCS", False)
    if api_docs:
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
