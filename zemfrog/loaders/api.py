from importlib import import_module

from flask import Blueprint, Flask

from ..helper import get_import_name, import_attr


def loader(app: Flask):
    """
    A function to load all of your API resources to flask based on the ``APIS`` configuration in config.py.
    """

    apis = app.config.get("APIS", [])
    import_name = get_import_name(app)
    api: Blueprint = import_attr(import_name + "apis.api")
    prefix = "apis."
    for name in apis:
        res = name
        if not name.startswith(prefix):
            res = prefix + res

        try:
            res = import_module(import_name + res)
        except ImportError:
            res = import_module(name.lstrip(prefix))

        endpoint = res.endpoint
        url_prefix = res.url_prefix
        routes = res.routes
        for detail in routes:
            route, view, methods = detail
            url = url_prefix + route
            e = endpoint + "_" + view.__name__
            api.add_url_rule(url, e, view_func=view, methods=methods)

    app.register_blueprint(api)
