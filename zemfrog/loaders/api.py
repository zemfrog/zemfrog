from importlib import import_module

from flask import Flask
from flask_smorest import Blueprint
from ..globals import smorest
from ..helper import get_import_name


def loader(app: Flask):
    """
    A function to load all of your API resources to flask based on the ``APIS`` configuration in config.py.
    """

    apis = app.config.get("APIS", [])
    import_name = get_import_name(app)
    api_prefix = app.config.get("API_PREFIX", "/api")
    prefix = "apis."
    for name in apis:
        res = name
        if not name.startswith(prefix):
            res = prefix + res

        try:
            res = import_module(import_name + res)
        except ImportError:
            res = import_module(name.lstrip(prefix))

        tag = res.tag
        description = res.description
        url_prefix = res.url_prefix
        bp = Blueprint(
            tag, __name__, url_prefix=api_prefix + url_prefix, description=description
        )
        routes = res.routes
        for detail in routes:
            url, view, methods = detail
            bp.route(url, methods=methods)(view)

        smorest.register_blueprint(bp)
