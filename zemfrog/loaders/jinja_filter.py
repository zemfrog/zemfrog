from flask import Flask

from ..helper import get_import_name, import_attr


def loader(app: Flask):
    """
    A function to load all jinja filters into a flask.
    """

    filters = app.config.get("JINJA_FILTERS", [])
    import_name = get_import_name(app)
    prefix = "filters."
    for name in filters:
        if not name.startswith(prefix):
            name = prefix + name

        name += ".init_filter"

        try:
            func = import_attr(import_name + name)
        except (ImportError, AttributeError):
            func = import_attr(name.lstrip(prefix))

        jinja_filters = func().items()
        for key, func in jinja_filters:
            app.jinja_env.filters[key] = func
