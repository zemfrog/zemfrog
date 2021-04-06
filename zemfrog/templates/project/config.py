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
    API_TITLE = "API Docs"
    API_VERSION = "v1"
    API_PREFIX = "/api"
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_JSON_PATH = "openapi.json"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_URL = "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    API_SPEC_OPTIONS = {
        'info': {
            'description': 'Powered by [zemfrog](https://github.com/zemfrog/zemfrog) + [flask-smorest](https://flask-smorest.readthedocs.io/en/latest/).',
            'contact' : {
                'email': 'hijriyan23@gmail.com'
            },
            'license': {
                'name': 'MIT License',
                'url': 'https://wikipedia.org/wiki/Licence_MIT'
            }
        }
    }
    API_SECURITY_DEFINITIONS = {
        "Bearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/jwt/login"
                }
            }
        }
    }
    API_SECURITY_PARAMS = [{"Bearer": []}]
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
        "zemfrog.extensions.smorest",
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
    BLUEPRINTS = []
    STATICFILES = []
    MIDDLEWARES = []
    APIS = []
    ERROR_HANDLERS = {}
    TASKS = ["zemfrog.tasks"]
    CONTEXT_PROCESSORS = []
    JINJA_FILTERS = []
    API_DOCS = True
    CREATE_DB = True
    USER_MODEL = "models.user.User"
    ROLE_MODEL = "models.user.Role"
    PERMISSION_MODEL = "models.user.Permission"
    LOG_MODEL = "models.user.Log"
    LOADERS = [
        "zemfrog.loaders.extension",
        "zemfrog.loaders.staticfile",
        "zemfrog.loaders.model",
        "zemfrog.loaders.blueprint",
        "zemfrog.loaders.middleware",
        "zemfrog.loaders.api",
        "zemfrog.loaders.error_handler",
        "zemfrog.loaders.command",
        "zemfrog.loaders.task",
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
