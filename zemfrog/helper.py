import os
from distutils.dir_util import copy_tree
from importlib import import_module
from types import ModuleType

from flask import Flask, current_app, render_template
from flask_sqlalchemy import Model

from .exception import ZemfrogModelNotFound, ZemfrogTemplateNotFound
from .globals import db

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

    db.session.add(model)
    db_commit()


def db_delete(model):
    """
    Functions to delete data in the database.
    """

    db.session.delete(model)
    db_commit()


def db_update(model, **kwds):
    """
    Function to update data in database.
    """

    columns = get_column_names(model)
    for k, v in kwds.items():
        if k in columns:
            setattr(model, k, v)
    db_commit()


def db_commit():
    """
    Functions for saving data to a database.
    """

    db.session.commit()


def get_mail_template(name, **context):
    r"""
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


def get_column_names(model):
    """
    Reference:
    * https://stackoverflow.com/questions/32927071/get-column-names-dynamically-with-sqlalchemy/33033067
    """

    columns = model.__table__.columns.keys()
    rels = model.__mapper__.relationships.keys()
    columns.extend(rels)
    return columns


def get_object_model(name):
    import_name = get_import_name(current_app)
    src = current_app.config[name.upper() + "_MODEL"]
    model = import_attr(import_name + src)
    return model
