import click
from flask.cli import with_appcontext

from ..generator import g_extension


@click.group("extension")
def group():
    """
    Extension generator.
    """


@group.command()
@with_appcontext
@click.argument("name")
def new(name):
    """
    Create extension.
    """

    g_extension(name)


command = group
