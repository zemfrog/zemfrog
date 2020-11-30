from flask import Flask
from importlib import import_module

from ..helper import get_import_name


def loader(app: Flask):
    """
    Function to load all celery tasks based on ``TASKS`` configuration in config.py.
    """

    dirname = "tasks"
    tasks = app.config.get(dirname.upper(), [])
    import_name = get_import_name(app)
    prefix = dirname + "."
    for name in tasks:
        sv = name
        if not name.startswith(prefix):
            sv = prefix + sv

        try:
            import_module(import_name + sv)
        except ImportError:
            import_module(sv)
