from flask import Flask
from flask_smorest import Blueprint

from ..globals import smorest
from ..helper import get_import_name, import_attr


def loader(app: Flask):
    """
    The function to load all blueprints based on the ``BLUEPRINTS`` configuration in config.py
    """

    blueprints = app.config.get("BLUEPRINTS", [])
    import_name = get_import_name(app)
    for name in blueprints:
        bp = name + ".routes.init_blueprint"
        routes = name + ".urls.routes"
        try:
            bp: Blueprint = import_attr(import_name + bp)()
            routes = import_attr(import_name + routes)
        except (ImportError, AttributeError):
            bp: Blueprint = import_attr(bp)()
            routes = import_attr(routes)

        for url, view, methods in routes:
            bp.route(url, methods=methods)(view)

        smorest.register_blueprint(bp)
