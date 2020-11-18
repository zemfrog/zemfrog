import os

from importlib import import_module
from distutils.dir_util import copy_tree
from types import ModuleType
from flask import current_app, Flask, render_template
from flask_sqlalchemy import Model

from .globals import current_db
from .exception import ZemfrogTemplateNotFound, ZemfrogModelNotFound

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


def get_template(*paths) -> str:
    """
    Function to get template base directory.

    :param paths: template directory or file name.

    :raises: ZemfrogTemplateNotFound

    """

    t = os.path.join(TEMPLATE_DIR, *paths)
    if not (os.path.isdir(t) or os.path.isfile(t)):
        raise ZemfrogTemplateNotFound("unknown template %r" % os.sep.join(paths))

    return t


def copy_template(name: str, dst: str):
    """
    Function for copying templates.

    :param name: template directory name.
    :param dst: Destination output.

    """

    t = get_template(name)
    copy_tree(t, dst)


def import_attr(module: str):
    """
    Functions to get attributes in modules.

    :param module: e.g. os.path

    """

    pkg, name = module.rsplit(".", 1)
    mod = import_module(pkg)
    return getattr(mod, name)


def search_model(name: str) -> str:
    """
    Function for getting the model location.

    :param name: model name.

    :raises: ZemfrogModelNotFound

    """

    for src, models in current_app.models.items():
        if name in models:
            return src

    raise ZemfrogModelNotFound("Cannot find %r orm model" % name)


def get_models(mod: ModuleType) -> list:
    """
    Function to get all ORM models in the module.

    :param mod: module object.

    """

    models = []
    childs = dir(mod)
    for c in childs:
        c = getattr(mod, c)
        try:
            if issubclass(c, Model):
                tbl_name = c.__name__
                models.append(tbl_name)
        except TypeError:
            pass

    return models


def db_add(model):
    """
    Functions for adding data to the database.
    """

    current_db.session.add(model)
    db_commit()


def db_delete(model):
    """
    Functions to delete data in the database.
    """

    current_db.session.delete(model)
    db_commit()


def db_update(model, **kwds):
    """
    Function to update data in database.
    """

    for k, v in kwds.items():
        setattr(model, k, v)
    db_commit()


def db_commit():
    """
    Functions for saving data to a database.
    """

    current_db.session.commit()


def get_mail_template(name, **context):
    """
    Functions to get email templates.

    :param name: email template name.
    :param \*\*context: jinja context.

    """

    tmp = render_template("emails/" + name, **context)
    return tmp


def get_import_name(app: Flask) -> str:
    import_name = (
        ""
        if not app.import_name.endswith(".wsgi")
        else app.import_name.rstrip(".wsgi") + "."
    )
    return import_name


def get_user_roles(user):
    roles = {}
    for role in user.roles:
        permissions = [perm.name for perm in role.permissions]
        roles[role.name] = permissions
    return roles
