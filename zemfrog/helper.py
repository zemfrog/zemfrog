import os

from importlib import import_module
from distutils.dir_util import copy_tree
from types import ModuleType
from jinja2 import Template
from flask import current_app
from flask_sqlalchemy import Model

from .exception import ZemfrogTemplateNotFound, ZemfrogModelNotFound

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


def get_template(name: str) -> str:
    """
    Function to get template base directory.

    :param name: template directory name.

    :raises: ZemfrogTemplateNotFound

    """

    t = os.path.join(TEMPLATE_DIR, name)
    if not os.path.isdir(t):
        raise ZemfrogTemplateNotFound("unknown template %r" % name)

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


def db_add(db, model):
    """
    Functions for adding data to the database.
    """

    db.session.add(model)
    db_commit(db)


def db_delete(db, model):
    """
    Functions to delete data in the database.
    """

    db.session.delete(model)
    db_commit(db)


def db_update(db, model, **kwds):
    """
    Function to update data in database.
    """

    for k, v in kwds.items():
        setattr(model, k, v)
    db_commit(db)


def db_commit(db):
    """
    Functions for saving data to a database.
    """

    db.session.commit()


def get_mail_template(name, **context):
    """
    Functions to get email templates.

    :param name: email template name.
    :param \*\*context: jinja context.

    :raises: ZemfrogTemplateNotFound

    """

    tmp_src = os.path.join("mail", name)
    if not os.path.isfile(tmp_src):
        raise ZemfrogTemplateNotFound("Email template %r was not found" % name)

    with open(tmp_src) as fp:
        data = fp.read()

    t = Template(data)
    tmp = t.render(**context)
    return tmp
