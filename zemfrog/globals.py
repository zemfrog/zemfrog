from flask import current_app
from werkzeug.local import LocalProxy


def _get_current_db():
    db = current_app.extensions["sqlalchemy"].db
    return db


current_db = LocalProxy(_get_current_db)
