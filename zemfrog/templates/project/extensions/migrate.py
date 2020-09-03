from flask_migrate import Migrate
from .sqlalchemy import db

migrate = Migrate(db=db)
init_app = migrate.init_app
