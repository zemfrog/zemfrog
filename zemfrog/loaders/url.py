from flask import Flask

from ..helper import get_import_name, import_attr


def loader(app: Flask):
    """
    This function will load all urls in the main application.
    """

    import_name = get_import_name(app)
    routes = import_attr(import_name + "urls.routes")
    for url, view, methods in routes:
        app.add_url_rule(url, view_func=view, methods=methods)
