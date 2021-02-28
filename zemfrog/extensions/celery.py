from zemfrog.app import make_celery
from flask import Flask


def init_app(app: Flask):
    celery = make_celery(app)
    app.extensions["celery"] = celery
