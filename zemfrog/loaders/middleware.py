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
        if not name.startswith(prefix):
            name = prefix + name

        name += ".init_middleware"
        try:
            middleware = import_attr(import_name + name)
        except (ImportError, AttributeError):
            middleware = import_attr(name.lstrip(prefix))

        app.wsgi_app = middleware(app.wsgi_app)
