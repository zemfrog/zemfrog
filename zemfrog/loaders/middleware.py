from flask import Flask

from ..helper import get_import_name, import_attr


def loader(app: Flask):
    """
    Function to load all middlewares.
    """

    middlewares = app.config.get("MIDDLEWARES", [])
    import_name = get_import_name(app)
    for name in middlewares:
        name = import_name + name + ".init_middleware"
        middleware = import_attr(name)
        app.wsgi_app = middleware(app.wsgi_app)
