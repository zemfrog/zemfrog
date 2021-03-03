import os
from glob import glob
from importlib import import_module

from flask import Flask

from ..helper import get_import_name, get_models


def loader(app: Flask):
    """
    A function to load all your ORM models in the ``models`` directory.
    """

    app.models = {}
    true = app.config.get("CREATE_DB")
    import_name = get_import_name(app)
    if import_name:
        import_name = import_name.replace(".", "/")

    if true:
        models = [
            x.rsplit(".", 1)[0].replace(os.sep, ".")
            for x in glob(import_name + "models/**/*.py", recursive=True)
        ]
        for m in models:
            if "__init__" in m:
                m = m.replace(".__init__", "")
            mod = import_module(m)
            app.models[m] = get_models(mod)

        app.extensions["sqlalchemy"].db.create_all()
