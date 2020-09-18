from flask import Flask
from . import loader
from celery import Celery


def make_celery(app: Flask):
    """
    Membuat aplikasi celery untuk aplikasi flask.
    Sumber https://flask.palletsprojects.com/en/1.1.x/patterns/celery/#configure
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


def create_app(name):
    """
    Fungsi untuk membuat aplikasi flask kamu.
    """

    app = Flask(name)

    with app.app_context():
        loader.load_config(app)
        loader.load_extensions(app)
        loader.load_models(app)
        loader.load_blueprints(app)
        loader.load_apis(app)
        loader.load_commands(app)
        loader.load_services(app)
        loader.load_docs(app)

    return app
