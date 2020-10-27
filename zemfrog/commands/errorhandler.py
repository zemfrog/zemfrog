import click
from flask.cli import with_appcontext
from ..generator import g_error_handler


@click.group("handler")
def group():
    """
    Error handler generator.
    """


@group.command()
@with_appcontext
@click.argument("name")
def new(name):
    """
    Create error handler.
    """

    g_error_handler(name)


command = group
