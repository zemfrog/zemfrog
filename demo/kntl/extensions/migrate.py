from flask_migrate import Migrate

migrate = Migrate()
init_app = migrate.init_app
