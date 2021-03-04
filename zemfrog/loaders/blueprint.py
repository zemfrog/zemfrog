from flask import Blueprint, Flask

from ..helper import get_import_name, import_attr


def loader(app: Flask):
    """
    The function to load all blueprints based on the ``BLUEPRINTS`` configuration in config.py
    """

    blueprints = app.config.get("BLUEPRINTS", [])
    import_name = get_import_name(app)
    for name in blueprints:
        bp = name + ".routes.blueprint"
        routes = name + ".urls.routes"
        try:
            bp: Blueprint = import_attr(import_name + bp)
            routes = import_attr(import_name + routes)
        except (ImportError, AttributeError):
            bp: Blueprint = import_attr(bp)
            routes = import_attr(routes)

        for url, view, methods in routes:
            bp.add_url_rule(url, view_func=view, methods=methods)

        app.register_blueprint(bp)
