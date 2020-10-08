import os
from flask.app import Flask
from flask_migrate import Migrate
from .sqlalchemy import db

migrate = Migrate(db=db)


def init_app(app: Flask):
    directory = os.path.join(app.root_path, "migrations")
    migrate.init_app(app, directory=directory)
