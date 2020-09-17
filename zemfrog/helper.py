import os

from importlib import import_module
from distutils.dir_util import copy_tree
from jinja2 import Template
from flask import current_app
from flask_sqlalchemy import Model

from .exception import ZemfrogTemplateNotFound, ZemfrogModelNotFound

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


def get_template(name):
    """
    Fungsi untuk mendapatkan base template.
    """

    t = os.path.join(TEMPLATE_DIR, name)
    if not os.path.isdir(t):
        raise ZemfrogTemplateNotFound("unknown template %r" % name)

    return t


def copy_template(name, dst):
    """
    Fungsi untuk menyalin template.
    """

    t = get_template(name)
    copy_tree(t, dst)


def import_attr(module):
    """
    Fungsi untuk mengambil atribut pada modul.
    """

    pkg, name = module.rsplit(".", 1)
    mod = import_module(pkg)
    return getattr(mod, name)


def search_model(name):
    """
    Fungsi untuk mendapatkan lokasi model.
    """

    for src, models in current_app.models.items():
        if name in models:
            return src

    raise ZemfrogModelNotFound("Tidak dapat menemukan model orm %r" % name)


def get_models(mod):
    """
    Fungsi untuk mendapatkan semua model ORM pada modul.
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
    Fungsi untuk menambahkan data ke database.
    """

    db.session.add(model)
    db_commit(db)


def db_delete(db, model):
    """
    Fungsi untuk menghapus data di database.
    """

    db.session.delete(model)
    db_commit(db)


def db_update(db, model, **kwds):
    """
    Fungsi untuk memperbaharui data di database.
    """

    for k, v in kwds.items():
        setattr(model, k, v)
    db_commit(db)


def db_commit(db):
    """
    Fungsi untuk menyimpan data ke database.
    """

    db.session.commit()


def get_mail_template(name, **context):
    """
    Fungsi untuk mendapatkan email template.
    """

    tmp_src = os.path.join("mail", name)
    if not os.path.isfile(tmp_src):
        raise ZemfrogTemplateNotFound("email template %r tidak ditemukan" % name)

    with open(tmp_src) as fp:
        data = fp.read()

    t = Template(data)
    tmp = t.render(**context)
    return tmp
