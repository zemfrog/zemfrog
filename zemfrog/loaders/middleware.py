from flask import Flask

from ..helper import get_import_name, import_attr


def loader(app: Flask):
    """
    Function to load all middlewares.
    """

    dirname = "middlewares"
    middlewares = app.config.get(dirname.upper(), [])
    import_name = get_import_name(app)
    prefix = dirname + "."
    for name in middlewares:
        mdl = name
        if not name.startswith(prefix):
            mdl = prefix + mdl

        try:
            name = import_name + mdl + ".init_middleware"
            middleware = import_attr(name)
        except (ImportError, AttributeError):
            name = mdl + ".init_middleware"
            middleware = import_attr(name)

        app.wsgi_app = middleware(app.wsgi_app)
