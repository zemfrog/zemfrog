import os
from flask import Flask
from os import getenv
from glob import glob
from importlib import import_module

from .generator import g_schema
from .exception import ZemfrogEnvironment
from .helper import import_attr, search_model

def load_config(app: Flask):
    env = getenv("ZEMFROG_ENV")
    if not env:
        raise ZemfrogEnvironment("environment not found")

    app.config.from_object("config." + env.capitalize())

def load_extensions(app: Flask):
    extensions = app.config.get("EXTENSIONS", [])
    for ext in extensions:
        ext = import_module(ext)
        init_func = getattr(ext, "init_app")
        init_func(app)

def load_models(app: Flask):
    app.models = {}
    true = app.config.get("CREATE_DB")
    if true:
        models = [x.rsplit(".", 1)[0].replace(os.sep, ".") for x in glob("models/**/*.py", recursive=True)]
        for m in models:
            if "__init__" in m:
                m = m.replace(".__init__", "")
            mod = import_module(m)
            app.models[mod] = m

        app.extensions["sqlalchemy"].db.create_all()

def load_commands(app: Flask):
    commands = app.config.get("COMMANDS", [])
    for cmd in commands:
        cmd = cmd + ".command"
        cmd = import_attr(cmd)
        app.cli.add_command(cmd)

def load_blueprints(app: Flask):
    blueprints = app.config.get("BLUEPRINTS", [])
    for bp in blueprints:
        bp = bp + ".routes.blueprint"
        bp = import_attr(bp)
        app.register_blueprint(bp)

def load_apis(app: Flask):
    apis = app.config.get("APIS", [])
    api = import_attr("api.api")
    for res in apis:
        res = import_attr(res) 
        api.add_resource(res)

    app.register_blueprint(api)

def load_services(app: Flask):
    services = app.config.get("SERVICES", [])
    for sv in services:
        import_module(sv)

def load_schemas(app: Flask):
    sql = app.extensions["sqlalchemy"]
    tables = sql.db.metadata.tables.keys()
    for t in tables:
        t = t.split("_")
        t = "".join([x.capitalize() for x in t])
        src = search_model(t)
        g_schema(t, src)
