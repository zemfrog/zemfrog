from flask import Flask

from ..helper import get_import_name, import_attr


def loader(app: Flask):
    """
    A function to load all context processors into a flask.
    """

    contexts = app.config.get("CONTEXT_PROCESSORS", [])
    import_name = get_import_name(app)
    prefix = "contexts."
    for name in contexts:
        if not name.startswith(prefix):
            name = prefix + name

        name += ".init_context"

        try:
            func = import_attr(import_name + name)
        except (ImportError, AttributeError):
            func = import_attr(name.lstrip(prefix))

        app.context_processor(func)
