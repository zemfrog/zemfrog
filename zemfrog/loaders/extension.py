from flask import Flask
from importlib import import_module

from ..helper import get_import_name


def loader(app: Flask):
    """
    The function to load all your flask extensions based on the ``EXTENSIONS`` configuration in config.py.
    """

    dirname = "extensions"
    extensions = app.config.get(dirname.upper(), [])
    import_name = get_import_name(app)
    prefix = dirname + "."
    for name in extensions:
        ext = name
        if not name.startswith(prefix):
            ext = prefix + ext

        try:
            ext = import_module(import_name + ext)
            init_func = getattr(ext, "init_app")
        except (ImportError, AttributeError):
            ext = import_module(ext)
            init_func = getattr(ext, "init_app")

        init_func(app)
