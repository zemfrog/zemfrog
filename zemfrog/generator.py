from importlib import import_module
import os
import string
import ast
import astor
import textwrap
from jinja2 import Template

from .helper import copy_template, search_model


def g_project(name: str):
    """
    Functions for creating projects.

    :param name: project name.

    """

    print("Creating %r project..." % name)
    copy_template("project", name)
    readme = os.path.join(name, "README.rst")
    with open(readme) as fp:
        data = fp.read()
        t = string.Template(data)
        new = t.safe_substitute(name=name)

    os.remove(readme)
    with open(readme, "w") as fp:
        fp.write(new)


def g_api(name: str):
    """
    Functions for creating APIs.

    :param name: REST API name.

    """

    print("Creating API %r... " % name, end="")
    copy_template("api", "api")
    old_filename = os.path.join("api", "name.py")
    with open(old_filename) as fp:
        old_data = fp.read()
        py_t = string.Template(old_data)
        new_data = py_t.safe_substitute(name=name, url_prefix=name.lower())

    os.remove(old_filename)
    new_filename = os.path.join("api", name.lower() + ".py")
    with open(new_filename, "w") as fp:
        fp.write(new_data)

    print("(done)")


def g_api_crud(name: str):
    """
    Function for creating REST API.

    :param name: REST API name.

    """

    src_model = search_model(name)
    src_schema = src_model.replace("models", "schema", 1)
    print("Creating REST API %r... " % name, end="")
    copy_template("crud", "api")
    old_filename = os.path.join("api", "name.py")
    with open(old_filename) as fp:
        old_data = fp.read()
        py_t = string.Template(old_data)
        new_data = py_t.safe_substitute(
            name=name,
            url_prefix=name.lower(),
            src_model=src_model,
            src_schema=src_schema,
        )

    os.remove(old_filename)
    new_filename = os.path.join("api", name.lower() + ".py")
    with open(new_filename, "w") as fp:
        fp.write(new_data)

    print("(done)")


def g_blueprint(name: str):
    """
    Function for creating blueprints.

    :param name: blueprint name.

    """

    print("Creating blueprint %r... " % name, end="")
    copy_template("blueprint", name.lower())
    for fname in ("routes", "urls"):
        filename = os.path.join(name.lower(), fname + ".py")
        with open(filename) as fp:
            old_data = fp.read()
            py_t = string.Template(old_data)
            new_data = py_t.safe_substitute(name=name)

        with open(filename, "w") as fp:
            fp.write(new_data)

    print("(done)")


def g_schema(src: str, models: list):
    """
    Function for creating schema models.

    :param src: source model.
    :param models: list of ORM models in your model module.

    """

    if not models:
        return

    srcfile = import_module(src).__file__.replace("models" + os.sep, "schema" + os.sep)
    if os.path.isfile(srcfile):
        with open(srcfile) as fp:
            data = fp.read()

        node_import = None
        klass = []
        root = ast.parse(data, filename=os.path.basename(srcfile))
        for node in ast.iter_child_nodes(root):
            if isinstance(node, ast.ImportFrom) and node.module == "models.user":
                node_import = node

            elif isinstance(node, ast.ClassDef):
                for b in node.bases:
                    if b.value.id == "ma" and node.name.endswith("Schema"):
                        name = node.name.replace("Schema", "")
                        klass.append(name)

        for k in klass:
            if k in models:
                models.remove(k)

        if models and node_import is not None:
            print("Creating schema for %r... " % src, end="")
            node_import.names = []
            for m in klass + models:
                m = ast.alias(name=m, asname=None)
                node_import.names.append(m)

            tmp = textwrap.dedent(
                """\
            {% for name in model_list %}
            class {{name}}Schema(ma.SQLAlchemyAutoSchema):
                class Meta:
                    model = {{name}}
            {% endfor %}
            """
            )
            t = Template(tmp)
            new_models = t.render(model_list=models)
            new_data = astor.to_source(root) + "\n" + new_models
            with open(srcfile, "w") as fp:
                fp.write(new_data)

            print("(done)")

        if klass:
            return

    print("Creating schema for %r... " % src, end="")
    copy_template("schema", "schema")
    old_filename = os.path.join("schema", "name.py")
    with open(old_filename) as fp:
        old_data = fp.read()
        t = Template(old_data)
        new_data = t.render(model_list=models, src_model=src)

    os.remove(old_filename)
    dirname = os.path.dirname(srcfile).replace("models" + os.sep, "schema" + os.sep)
    try:
        os.makedirs(dirname)
    except FileExistsError:
        pass

    with open(srcfile, "w") as fp:
        fp.write(new_data)

    print("(done)")


def g_command(name: str):
    """
    Function to create boilerplate command.

    :param name: command name.

    """

    print("Creating command %r..." % name, end="")
    copy_template("command", "commands")
    old_filename = os.path.join("commands", "name.py")
    with open(old_filename) as fp:
        old_data = fp.read()
        py_t = string.Template(old_data)
        new_data = py_t.safe_substitute(name=name)

    os.remove(old_filename)
    new_filename = os.path.join("commands", name.lower() + ".py")
    with open(new_filename, "w") as fp:
        fp.write(new_data)

    print("(done)")
