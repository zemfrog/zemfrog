import os

from importlib import import_module
from distutils.dir_util import copy_tree
from flask import current_app
from flask_sqlalchemy import Model

from .exception import ZemfrogTemplateNotFound

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")

def get_template(name):
    t = os.path.join(TEMPLATE_DIR, name)
    if not os.path.isdir(t):
        raise ZemfrogTemplateNotFound("unknown template %r" % name)

    return t

def copy_template(name, dst):
    t = get_template(name)
    copy_tree(t, dst)

def import_attr(module):
    pkg, name = module.rsplit(".", 1)
    mod = import_module(pkg)
    return getattr(mod, name)

def search_model(name):
    for mod in current_app.models:
        childs = dir(mod)
        for c in childs:
            c = getattr(mod, c)
            try:
                if issubclass(c, Model):
                    tbl_name = c.__name__
                    if tbl_name == name:
                        src = current_app.models.get(mod)
                        return src
            except TypeError:
                pass

def db_add(db, model):
    db.session.add(model)
    db.session.commit()

def db_delete(db, model):
    db.session.delete(model)
    db.session.commit()

def db_update(db, model, **kwds):
    for k, v in kwds.items():
        setattr(model, k, v)
    db.session.commit()
