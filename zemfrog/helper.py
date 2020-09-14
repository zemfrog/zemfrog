import os

from importlib import import_module
from distutils.dir_util import copy_tree
from jinja2 import Template
from flask import current_app
from flask_sqlalchemy import Model

from .exception import ZemfrogTemplateNotFound, ZemfrogModelNotFound

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
    for src, models in current_app.models:
        if name in models:
            return src

    raise ZemfrogModelNotFound("Tidak dapat menemukan model orm %r" % name)


def get_models(mod):
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
    db.session.add(model)
    db_commit(db)


def db_delete(db, model):
    db.session.delete(model)
    db_commit(db)


def db_update(db, model, **kwds):
    for k, v in kwds.items():
        setattr(model, k, v)
    db_commit(db)


def db_commit(db):
    db.session.commit()


def get_mail_template(name, **context):
    tmp_src = os.path.join("mail", name)
    if not os.path.isfile(tmp_src):
        raise ZemfrogTemplateNotFound("email template %r tidak ditemukan" % name)

    with open(tmp_src) as fp:
        data = fp.read()

    t = Template(data)
    tmp = t.render(**context)
    return tmp
