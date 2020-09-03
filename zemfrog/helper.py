import os

from importlib import import_module
from distutils.dir_util import copy_tree

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
