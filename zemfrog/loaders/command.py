import pkg_resources

from flask import Flask
from flask.cli import routes_command, run_command, shell_command

from ..helper import get_import_name, import_attr


def loader(app: Flask):
    """
    A function to load all your commands and register them in the ``flask`` command.
    """

    commands = app.config.get("COMMANDS", [])
    import_name = get_import_name(app)
    for name in commands:
        try:
            n = import_name + name + ".command"
            cmd = import_attr(n)
        except ImportError:
            n = name + ".command"
            cmd = import_attr(n)

        app.cli.add_command(cmd)

    if import_name:
        for cmd in (run_command, shell_command, routes_command):
            app.cli.add_command(cmd)

        for ep in pkg_resources.iter_entry_points("flask.commands"):
            app.cli.add_command(ep.load(), ep.name)
