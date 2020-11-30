from flask import Flask, Blueprint
from flask_apispec import FlaskApiSpec
from importlib import import_module

from ..decorators import api_doc
from ..helper import get_import_name, import_attr


def loader(app: Flask):
    """
    Function for creating api docs using ``flask-apispec``.
    """

    if not app.config.get("API_DOCS", False):
        return

    import_name = get_import_name(app)
    docs: FlaskApiSpec = import_attr(import_name + "extensions.apispec.docs")
    urls = import_module(import_name + "urls")
    docs_params = urls.docs
    routes = urls.routes
    for _, view, _ in routes:
        if docs_params:
            view = api_doc(**docs_params)(view)
        docs.register(view)

    apis = app.config.get("APIS", [])
    for res in apis:
        res = import_module(import_name + res)
        docs_params = res.docs
        routes = res.routes
        endpoint = res.endpoint
        for detail in routes:
            _, view, _ = detail
            e = endpoint + "_" + view.__name__
            if docs_params:
                view = api_doc(**docs_params)(view)
            docs.register(view, endpoint=e, blueprint="api")

    blueprints = app.config.get("BLUEPRINTS", [])
    for name in blueprints:
        bp = import_name + name + ".routes.blueprint"
        bp: Blueprint = import_attr(bp)
        urls = import_name + name + ".urls"
        urls = import_module(urls)
        docs_params = urls.docs
        routes = urls.routes
        for _, view, _ in routes:
            if docs_params:
                view = api_doc(**docs_params)(view)
            docs.register(view, blueprint=name)
