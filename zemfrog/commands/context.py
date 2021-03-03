import click
from flask.cli import with_appcontext

from ..generator import g_context


@click.group("context")
def group():
    """
    Context generator.
    """


@group.command()
@with_appcontext
@click.argument("name")
def new(name):
    """
    Create a new context.
    """

    g_context(name)


command = group
