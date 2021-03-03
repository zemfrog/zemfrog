import os
from importlib import import_module

from celery import Celery
from flask import Flask
from flask.cli import load_dotenv

from .exception import ZemfrogEnvironment
from .helper import get_import_name


def make_celery(app: Flask) -> Celery:
    """
    Creating a celery application for flask applications.
    Source: https://flask.palletsprojects.com/en/1.1.x/patterns/celery/#configure
    """

    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


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


def create_app(name: str) -> Flask:
    """
    Functions to build your flask application and load all configurations.

    :param name: import name.

    """

    app = Flask(name)
    import_name = get_import_name(app)
    dirname = "loaders"
    prefix = dirname + "."
    with app.app_context():
        load_config(app)
        for name in app.config.get(dirname.upper(), []):
            yourloader = name
            if not name.startswith(prefix):
                yourloader = prefix + yourloader

            try:
                yourloader = import_module(import_name + yourloader)
                loader = getattr(yourloader, "loader")
            except (ImportError, AttributeError):
                yourloader = import_module(name)
                loader = getattr(yourloader, "loader")

            loader(app)

    return app
