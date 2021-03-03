import pkg_resources
from flask import Flask
from flask.cli import routes_command, run_command, shell_command

from ..helper import get_import_name, import_attr


def loader(app: Flask):
    """
    A function to load all your commands and register them in the ``flask`` command.
    """

    dirname = "commands"
    commands = app.config.get(dirname.upper(), [])
    import_name = get_import_name(app)
    prefix = dirname + "."
    for name in commands:
        if not name.startswith(prefix):
            name = prefix + name

        name += ".command"
        try:
            cmd = import_attr(import_name + name)
        except ImportError:
            cmd = import_attr(name.lstrip(prefix))

        app.cli.add_command(cmd)

    if import_name:
        for cmd in (run_command, shell_command, routes_command):
            app.cli.add_command(cmd)

        for ep in pkg_resources.iter_entry_points("flask.commands"):
            app.cli.add_command(ep.load(), ep.name)
