from flask import Flask

from zemfrog.app import make_celery


def init_app(app: Flask):
    celery = make_celery(app)
    app.extensions["celery"] = celery
