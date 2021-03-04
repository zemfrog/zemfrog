from importlib import import_module

from flask import Flask

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
        if not name.startswith(prefix):
            name = prefix + name

        try:
            import_module(import_name + name)
        except ImportError:
            import_module(name.lstrip(prefix))
