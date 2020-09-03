class Development(object):
    SECRET_KEY = "Your secret key!"
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    EXTENSIONS = ["sqlalchemy", "migrate"]
    COMMANDS = []
    BLUEPRINTS = []
    CELERY_RESULT_BACKEND = None
    CELERY_BROKER_URL = None

class Production(Development):
    DEBUG = False

class Testing(Development):
    TESTING = True
