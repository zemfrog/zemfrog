from flask import Flask

from ..helper import get_import_name, import_attr


def loader(app: Flask):
    """
    The function to load all your flask extensions based on the ``EXTENSIONS`` configuration in config.py.
    """

    dirname = "extensions"
    extensions = app.config.get(dirname.upper(), [])
    import_name = get_import_name(app)
    prefix = dirname + "."
    for name in extensions:
        if not name.startswith(prefix):
            name = prefix + name

        name += ".init_app"
        try:
            init_func = import_attr(import_name + name)
        except (ImportError, AttributeError):
            init_func = import_attr(name.lstrip(prefix))

        init_func(app)
