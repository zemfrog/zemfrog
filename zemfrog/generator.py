from importlib import import_module
import os
import string
import ast
import astor
import textwrap
from flask.globals import current_app
from jinja2 import Template

from .helper import copy_template, get_import_name, search_model


def g_project(name: str, import_name: str):
    """
    Functions for creating projects.

    :param name: project name.

    """

    print("Creating %r project... " % name, end="")
    copy_template("project", name)
    main_app = True if import_name == "wsgi" else False
    for root, _, files in os.walk(name):
        for f in files:
            if not f.endswith((".py", ".rst")):
                continue

            f = os.path.join(root, f)
            with open(f) as fp:
                data = fp.read()
                t = Template(data)
                new = t.render(import_name=import_name, main_app=main_app, name=name)

            with open(f, "w") as fp:
                fp.write(new)

    print("(done)")


def g_api(name: str):
    """
    Functions for creating APIs.

    :param name: REST API name.

    """

    print("Creating API %r... " % name, end="")
    api_dir = os.path.join(current_app.root_path, "api")
    copy_template("api", api_dir)
    old_filename = os.path.join(api_dir, "name.py")
    with open(old_filename) as fp:
        old_data = fp.read()
        py_t = string.Template(old_data)
        new_data = py_t.safe_substitute(name=name, url_prefix=name.lower())

    os.remove(old_filename)
    new_filename = os.path.join(api_dir, name.lower() + ".py")
    with open(new_filename, "w") as fp:
        fp.write(new_data)

    print("(done)")


def g_api_crud(name: str):
    """
    Function for creating REST API.

    :param name: REST API name.

    """

    src_model = search_model(name)
    import_name = get_import_name(current_app)
    main_app = True
    if import_name:
        main_app = False
        idx = len(import_name)
        src_model = src_model[idx:]

    src_schema = src_model.replace("models", "schema", 1)
    api_dir = os.path.join(current_app.root_path, "api")
    print("Creating REST API %r... " % name, end="")
    copy_template("crud", api_dir)
    old_filename = os.path.join(api_dir, "name.py")
    with open(old_filename) as fp:
        old_data = fp.read()
        py_t = Template(old_data)
        new_data = py_t.render(
            name=name,
            url_prefix=name.lower(),
            src_model=src_model,
            src_schema=src_schema,
            main_app=main_app,
        )

    os.remove(old_filename)
    new_filename = os.path.join(api_dir, name.lower() + ".py")
    with open(new_filename, "w") as fp:
        fp.write(new_data)

    print("(done)")


def g_blueprint(name: str):
    """
    Function for creating blueprints.

    :param name: blueprint name.

    """

    print("Creating blueprint %r... " % name, end="")
    bp_dir = os.path.join(current_app.root_path, name.lower())
    copy_template("blueprint", bp_dir)
    for fname in ("routes", "urls"):
        filename = os.path.join(bp_dir, fname + ".py")
        with open(filename) as fp:
            old_data = fp.read()
            py_t = string.Template(old_data)
            new_data = py_t.safe_substitute(name=name)

        with open(filename, "w") as fp:
            fp.write(new_data)

    print("(done)")


def g_middleware(name: str):
    """
    Function for creating middleware.

    :param str name: middleware name.

    """

    print("Creating middleware %r... " % name, end="")
    middleware_dir = os.path.join(current_app.root_path, "middlewares")
    copy_template("middleware", middleware_dir)
    old_filename = os.path.join(middleware_dir, "name.py")
    new_filename = os.path.join(middleware_dir, name.lower() + ".py")
    os.rename(old_filename, new_filename)
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
    import_name = get_import_name(current_app).rstrip(".")
    main_app = True
    if import_name:
        main_app = False
        idx = len(import_name) + 1
        src = src[idx:]

    schema_dir = os.path.join(current_app.root_path, "schema")
    copy_template("schema", schema_dir)
    old_filename = os.path.join(schema_dir, "name.py")
    with open(old_filename) as fp:
        old_data = fp.read()
        t = Template(old_data)
        new_data = t.render(main_app=main_app, model_list=models, src_model=src)

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
    cmd_dir = os.path.join(current_app.root_path, "commands")
    copy_template("command", cmd_dir)
    old_filename = os.path.join(cmd_dir, "name.py")
    with open(old_filename) as fp:
        old_data = fp.read()
        py_t = string.Template(old_data)
        new_data = py_t.safe_substitute(name=name)

    os.remove(old_filename)
    new_filename = os.path.join(cmd_dir, name.lower() + ".py")
    with open(new_filename, "w") as fp:
        fp.write(new_data)

    print("(done)")
