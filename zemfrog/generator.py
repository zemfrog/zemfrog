import os
from flask.globals import current_app
from jinja2 import Template

from .helper import copy_template, get_import_name, get_template, search_model
from .validators import validate_module_name


def g_project(name: str, import_name: str):
    """
    Functions for creating projects.

    :param name: project name.

    """

    validate_module_name(name)
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


def g_extension(name: str):
    """
    Function for making extension boilerplate.

    :param name: extension name.
    """

    validate_module_name(name)
    print("Creating a %r extension..." % name, end="")
    ext_dir = os.path.join(current_app.root_path, "extensions")
    old_filename = get_template("extension", "name.py")
    with open(old_filename) as fp:
        new_data = fp.read()

    new_filename = os.path.join(ext_dir, name.lower() + ".py")
    with open(new_filename, "w") as fp:
        fp.write(new_data)

    print("(done)")


def g_task(name: str):
    """
    Function for creating celery task.

    :param name: task name.
    """

    validate_module_name(name)
    print("Creating %r task..." % name, end="")
    import_name = get_import_name(current_app)
    main_app = True
    if import_name:
        main_app = False

    ext_dir = os.path.join(current_app.root_path, "tasks")
    old_filename = get_template("task", "name.py")
    with open(old_filename) as fp:
        old_data = fp.read()
        py_t = Template(old_data)
        new_data = py_t.render(main_app=main_app, task_name=name)

    new_filename = os.path.join(ext_dir, name.lower() + ".py")
    with open(new_filename, "w") as fp:
        fp.write(new_data)

    print("(done)")


def g_model(name: str):
    """
    Function for creating sqlalchemy model.

    :param name: model name.
    """

    validate_module_name(name)
    print("Creating %r model..." % name, end="")
    import_name = get_import_name(current_app)
    main_app = True
    if import_name:
        main_app = False

    model_dir = os.path.join(current_app.root_path, "models")
    old_filename = get_template("model", "name.py")
    with open(old_filename) as fp:
        old_data = fp.read()
        py_t = Template(old_data)
        new_data = py_t.render(main_app=main_app, model_name=name.capitalize())

    new_filename = os.path.join(model_dir, name.lower() + ".py")
    with open(new_filename, "w") as fp:
        fp.write(new_data)

    print("(done)")


def g_api(name: str):
    """
    Functions for creating APIs.

    :param name: REST API name.

    """

    validate_module_name(name)
    print("Creating API %r... " % name, end="")
    api_dir = os.path.join(current_app.root_path, "api")
    old_filename = get_template("api", "name.py")
    with open(old_filename) as fp:
        old_data = fp.read()
        py_t = Template(old_data)
        new_data = py_t.render(name=name, url_prefix=name.lower())

    new_filename = os.path.join(api_dir, name.lower() + ".py")
    with open(new_filename, "w") as fp:
        fp.write(new_data)

    print("(done)")


def g_api_crud(name: str):
    """
    Function for creating REST API.

    :param name: REST API name.

    """

    validate_module_name(name)
    src_model = search_model(name)
    import_name = get_import_name(current_app)
    main_app = True
    if import_name:
        main_app = False
        idx = len(import_name)
        src_model = src_model[idx:]

    api_dir = os.path.join(current_app.root_path, "api")
    print("Creating REST API %r... " % name, end="")
    old_filename = get_template("crud", "name.py")
    with open(old_filename) as fp:
        old_data = fp.read()
        py_t = Template(old_data)
        new_data = py_t.render(
            name=name,
            url_prefix=name.lower(),
            src_model=src_model,
            main_app=main_app,
        )

    new_filename = os.path.join(api_dir, name.lower() + ".py")
    with open(new_filename, "w") as fp:
        fp.write(new_data)

    print("(done)")


def g_blueprint(name: str):
    """
    Function for creating blueprints.

    :param name: blueprint name.

    """

    validate_module_name(name)
    print("Creating blueprint %r... " % name, end="")
    bp_dir = os.path.join(current_app.root_path, name.lower())
    copy_template("blueprint", bp_dir)
    for fname in ("routes", "urls"):
        filename = os.path.join(bp_dir, fname + ".py")
        with open(filename) as fp:
            old_data = fp.read()
            py_t = Template(old_data)
            new_data = py_t.render(name=name)

        with open(filename, "w") as fp:
            fp.write(new_data)

    print("(done)")


def g_middleware(name: str):
    """
    Function for creating middleware.

    :param str name: middleware name.

    """

    validate_module_name(name)
    print("Creating middleware %r... " % name, end="")
    middleware_dir = os.path.join(current_app.root_path, "middlewares")
    old_filename = get_template("middleware", "name.py")
    with open(old_filename) as fp:
        data = fp.read()

    new_filename = os.path.join(middleware_dir, name.lower() + ".py")
    with open(new_filename, "w") as fp:
        fp.write(data)

    print("(done)")


def g_command(name: str):
    """
    Function to create boilerplate command.

    :param name: command name.

    """

    validate_module_name(name)
    print("Creating command %r..." % name, end="")
    cmd_dir = os.path.join(current_app.root_path, "commands")
    old_filename = get_template("command", "name.py")
    with open(old_filename) as fp:
        old_data = fp.read()
        py_t = Template(old_data)
        new_data = py_t.render(name=name)

    new_filename = os.path.join(cmd_dir, name.lower() + ".py")
    with open(new_filename, "w") as fp:
        fp.write(new_data)

    print("(done)")


def g_error_handler(name):
    """
    Function for creating error handler.

    :param str name: name of the handler.

    """

    validate_module_name(name)
    print("Creating error handler %r... " % name, end="")
    eh_dir = os.path.join(current_app.root_path, "handlers")
    old_filename = get_template("errorhandler", "name.py")
    with open(old_filename) as fp:
        data = fp.read()

    new_filename = os.path.join(eh_dir, name.lower() + ".py")
    with open(new_filename, "w") as fp:
        fp.write(data)

    print("(done)")
