from flask import Flask

from ..helper import get_import_name, import_attr


def loader(app: Flask):
    """
    Function to load all error handlers
    """

    import_name = get_import_name(app)
    handlers = app.config.get("ERROR_HANDLERS", {})
    for code, view in handlers.items():
        view = import_attr(import_name + view + ".handler")
        app.register_error_handler(code, view)
