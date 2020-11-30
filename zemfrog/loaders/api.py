from flask import Flask, Blueprint
from importlib import import_module

from ..helper import get_import_name, import_attr


def loader(app: Flask):
    """
    A function to load all of your API resources to flask based on the ``APIS`` configuration in config.py.
    """

    apis = app.config.get("APIS", [])
    import_name = get_import_name(app)
    api: Blueprint = import_attr(import_name + "api.api")
    for res in apis:
        res = import_module(import_name + res)
        endpoint = res.endpoint
        url_prefix = res.url_prefix
        routes = res.routes
        for detail in routes:
            route, view, methods = detail
            url = url_prefix + route
            e = endpoint + "_" + view.__name__
            api.add_url_rule(url, e, view_func=view, methods=methods)

    app.register_blueprint(api)
