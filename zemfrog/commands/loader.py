import click
from flask.cli import with_appcontext

from ..generator import g_loader


@click.group("loader")
def group():
    """
    Loader generator.
    """


@group.command()
@with_appcontext
@click.argument("name")
def new(name):
    """
    Create a new loader.
    """

    g_loader(name)


command = group
