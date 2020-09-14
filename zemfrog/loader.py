import os
from flask import Flask
from os import getenv
from glob import glob
from importlib import import_module

from flask.cli import load_dotenv
from flask.blueprints import Blueprint

from .generator import g_schema
from .exception import ZemfrogEnvironment
from .helper import get_models, import_attr, search_model


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
    Semua ekstensi flask kamu berada di folder ``extensions``
    dan itu akan secara otomatis dimuat semua oleh zemfrog.

    .. note::
        Ekstensi harus mempunyai method ``init_app`` pada modul kamu.
        Untuk contoh kamu bisa liat salah satu modul di folder ``ekstensions``.
    """

    extensions = app.config.get("EXTENSIONS", [])
    for ext in extensions:
        ext = import_module(ext)
        init_func = getattr(ext, "init_app")
        init_func(app)


def load_models(app: Flask):
    """
    Semua model ORM sqlalchemy kamu berada di folder ``models``
    dan itu akan secara otomatis dimuat semua oleh zemfrog.

    .. note::
        Secara bawaan semua model yg ada di folder ``models``
        akan dibuat semua ke bentuk table di database.
        Kamu bisa menonaktifkan pembuatan table dengan mengatur nilai ``False``
        pada konfigurasi ``CREATE_DB``.
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
    Di zemfrog, kamu dapat membuat command kamu sendiri dan mendaftarkanya pada command ``flask``.

    .. note::
        Kamu dapat membuat ``boilerplate command`` dengan menggunakan command ``flask command new``.
        Dan jangan lupa untuk mendaftarkan nya ke konfigurasi ``COMMANDS``.
    """

    commands = app.config.get("COMMANDS", [])
    for cmd in commands:
        cmd = cmd + ".command"
        cmd = import_attr(cmd)
        app.cli.add_command(cmd)


def load_blueprints(app: Flask):
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
    services = app.config.get("SERVICES", [])
    for sv in services:
        import_module(sv)


def load_schemas(app: Flask):
    for src, models in app.models.items():
        g_schema(src, models)
