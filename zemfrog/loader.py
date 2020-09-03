from flask import Flask
from os import getenv, listdir
from importlib import import_module

from .generator import g_schema
from .exception import ZemfrogEnvironment

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
    true = app.config.get("CREATE_DB")
    if true:
        models = listdir("models")
        models.remove("__init__.py")
        for m in models:
            m = "models." + m
            import_module(m)

def load_commands(app: Flask):
    commands = app.config.get("COMMANDS", [])
    for cmd in commands:
        cmd = import_module(cmd)
        cmd = getattr(cmd, "command")
        app.cli.add_command(cmd)

def load_blueprints(app: Flask):
    blueprints = app.config.get("BLUEPRINTS", [])
    for bp in blueprints:
        bp = import_module(bp)
        bp = getattr(bp, "blueprint")
        app.register_blueprint(bp)

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
        g_schema(t)
