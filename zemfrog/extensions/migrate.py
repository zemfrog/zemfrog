import os

from flask.app import Flask
from flask_migrate import Migrate

from ..globals import db


def init_app(app: Flask):
    migrate = Migrate(db=db)
    directory = os.path.join(
        app.root_path, "migrations/" + os.getenv("ZEMFROG_ENV", "development").lower()
    )
    migrate.init_app(app, directory=directory)
