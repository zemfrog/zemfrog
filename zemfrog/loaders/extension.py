from flask import Flask
from importlib import import_module

from ..helper import get_import_name


def loader(app: Flask):
    """
    The function to load all your flask extensions based on the ``EXTENSIONS`` configuration in config.py.
    """

    extensions = app.config.get("EXTENSIONS", [])
    import_name = get_import_name(app)
    for ext in extensions:
        ext = import_module(import_name + ext)
        init_func = getattr(ext, "init_app")
        init_func(app)
