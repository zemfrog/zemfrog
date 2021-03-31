from importlib import import_module

from flask import Flask
from flask.blueprints import Blueprint

from zemfrog.globals import apispec as docs

from ..decorators import api_doc
from ..helper import get_import_name, import_attr


def loader(app: Flask):
    """
    Function for creating api docs using ``flask-apispec``.
    """

    if not app.config.get("API_DOCS", False):
        return

    import_name = get_import_name(app)
    urls = import_module(import_name + "urls")
    docs_params = urls.docs
    routes = urls.routes
    for _, view, _ in routes:
        if docs_params:
            view = api_doc(**docs_params)(view)
        docs.register(view)

    apis = app.config.get("APIS", [])
    api_prefix = "apis."
    for name in apis:
        if not name.startswith(api_prefix):
            name = api_prefix + name

        try:
            res = import_module(import_name + name)
        except ImportError:
            res = import_module(name.lstrip(api_prefix))

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
        bp = name + ".routes.init_blueprint"
        urls = name + ".urls"
        try:
            urls = import_module(import_name + urls)
            bp: Blueprint = import_attr(import_name + bp)()
        except (ImportError, AttributeError):
            urls = import_module(urls)
            bp: Blueprint = import_attr(bp)()

        name = bp.name
        docs_params = urls.docs
        routes = urls.routes

        for _, view, _ in routes:
            if docs_params:
                view = api_doc(**docs_params)(view)
            docs.register(view, blueprint=name)
