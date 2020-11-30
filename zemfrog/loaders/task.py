from flask import Flask
from importlib import import_module

from ..helper import get_import_name


def loader(app: Flask):
    """
    Function to load all celery tasks based on ``TASKS`` configuration in config.py.
    """

    tasks = app.config.get("TASKS", [])
    import_name = get_import_name(app)
    for sv in tasks:
        import_module(import_name + sv)
