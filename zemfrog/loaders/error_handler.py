from flask import Flask

from ..helper import get_import_name, import_attr


def loader(app: Flask):
    """
    Function to load all error handlers
    """

    import_name = get_import_name(app)
    handlers = app.config.get("ERROR_HANDLERS", {})
    prefix = "handlers."
    for code, func in handlers.items():
        if not func.startswith(prefix):
            func = prefix + func
        func += ".handler"
        try:
            view = import_attr(import_name + func)
        except (ImportError, AttributeError):
            view = import_attr(func.lstrip(prefix))

        app.register_error_handler(code, view)
