from datetime import timedelta
from os import path

class Development(object):
    SECRET_KEY = "Your secret key!"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(
        path.dirname(__file__), "db.sqlite"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "JWT secret key!"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    MAIL_PORT = 8025
    MAIL_DEFAULT_SENDER = "admin@localhost.com"
    APISPEC_TITLE = "API Docs"
    APISPEC_SWAGGER_UI_URL = "/docs"
    APISPEC_SECURITY_DEFINITIONS = {
        "Bearer": {
            "type": "oauth2",
            "flow": "password",
            "tokenUrl": "/auth/jwt/login",
        }
    }
    APISPEC_SECURITY_PARAMS = [{"Bearer": []}]
    DEBUG = True
    {% if main_app -%}
        APPS = []
    {%- endif %}
    EXTENSIONS = [
        "zemfrog.extensions.sqlalchemy",
        "zemfrog.extensions.marshmallow",
        "zemfrog.extensions.migrate",
        "zemfrog.extensions.jwt",
        "zemfrog.extensions.mail",
        "zemfrog.extensions.celery",
        "zemfrog.extensions.apispec",
        "zemfrog.extensions.cors"
    ]
    COMMANDS = [
        "zemfrog.commands.api",
        "zemfrog.commands.blueprint",
        "zemfrog.commands.middleware",
        "zemfrog.commands.command",
        "zemfrog.commands.errorhandler",
        "zemfrog.commands.extension",
        "zemfrog.commands.model",
        "zemfrog.commands.task",
        "zemfrog.commands.user",
        "zemfrog.commands.role",
        "zemfrog.commands.permission",
        "zemfrog.commands.loader",
        "zemfrog.commands.secretkey",
        "zemfrog.commands.context",
        "zemfrog.commands.filter",
        {% if main_app -%}
            "zemfrog.commands.app"
        {%- endif %}
    ]
    BLUEPRINTS = ["auth"]
    STATICFILES = []
    MIDDLEWARES = []
    APIS = []
    ERROR_HANDLERS = {422: "api_errors", 400: "api_errors"}
    TASKS = []
    CONTEXT_PROCESSORS = []
    JINJA_FILTERS = []
    API_DOCS = True
    CREATE_DB = True
    USER_MODEL = "models.user.User"
    ROLE_MODEL = "models.user.Role"
    PERMISSION_MODEL = "models.user.Permission"
    LOADERS = [
        "zemfrog.loaders.extension",
        "zemfrog.loaders.staticfile",
        "zemfrog.loaders.model",
        "zemfrog.loaders.url",
        "zemfrog.loaders.blueprint",
        "zemfrog.loaders.middleware",
        "zemfrog.loaders.api",
        "zemfrog.loaders.error_handler",
        "zemfrog.loaders.command",
        "zemfrog.loaders.task",
        "zemfrog.loaders.openapi",
        "zemfrog.loaders.context_processor",
        "zemfrog.loaders.jinja_filter",
        "zemfrog.loaders.multiapp",
    ]
    CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379"
    CELERY_BROKER_URL = CELERY_RESULT_BACKEND


class Production(Development):
    DEBUG = False
    JWT_COOKIE_SECURE = True


class Testing(Development):
    TESTING = True
