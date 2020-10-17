import click
from flask.cli import with_appcontext
from ..generator import g_command


@click.group("command")
def group():
    """
    Command generator.
    """


@group.command()
@with_appcontext
@click.argument("name")
def new(name):
    """
    Create command.
    """

    g_command(name)


command = group
