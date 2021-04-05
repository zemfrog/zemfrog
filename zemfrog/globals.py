from flask import current_app
from flask_marshmallow import EXTENSION_NAME
from werkzeug.local import LocalProxy


def _get_db():
    db = current_app.extensions["sqlalchemy"].db
    return db


def _get_smorest():
    api = current_app.extensions["flask-smorest"]["ext_obj"]
    return api


def _get_celery():
    celery = current_app.extensions["celery"]
    return celery


def _get_mail():
    mail = current_app.extensions["mail"]
    return mail


def _get_marshmallow():
    ma = current_app.extensions[EXTENSION_NAME]
    return ma


def _get_migrate():
    migrate = current_app.extensions["migrate"]
    return migrate


db = LocalProxy(_get_db)
smorest = LocalProxy(_get_smorest)
celery = LocalProxy(_get_celery)
mail = LocalProxy(_get_mail)
ma = LocalProxy(_get_marshmallow)
migrate = LocalProxy(_get_migrate)
