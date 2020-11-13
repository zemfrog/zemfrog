from flask import Flask
from . import loader
from celery import Celery


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


def create_app(name: str) -> Flask:
    """
    Functions to build your flask application and load all configurations.

    :param name: import name.

    """

    app = Flask(name)
    with app.app_context():
        loader.load_config(app)
        loader.load_extensions(app)
        loader.load_staticfiles(app)
        loader.load_models(app)
        loader.load_urls(app)
        loader.load_blueprints(app)
        loader.load_middlewares(app)
        loader.load_apis(app)
        loader.load_error_handlers(app)
        loader.load_commands(app)
        loader.load_tasks(app)
        loader.load_docs(app)
        loader.load_apps(app)

    return app
