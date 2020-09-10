class Development(object):
    SECRET_KEY = "Your secret key!"
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    EXTENSIONS = [
        "extensions.sqlalchemy",
        "extensions.marshmallow",
        "extensions.migrate"
    ]
    COMMANDS = [
        "zemfrog.commands.api",
        "zemfrog.commands.blueprint",
        "zemfrog.commands.schema",
        "zemfrog.commands.command"
    ]
    BLUEPRINTS = []
    APIS = []
    CREATE_DB = True
    CELERY_RESULT_BACKEND = None
    CELERY_BROKER_URL = None

class Production(Development):
    DEBUG = False

class Testing(Development):
    TESTING = True
