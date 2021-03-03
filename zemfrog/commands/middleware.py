import click
from flask.cli import with_appcontext

from ..generator import g_middleware


@click.group("middleware")
def group():
    """
    Middleware generator.
    """


@group.command()
@with_appcontext
@click.argument("name")
def new(name):
    """
    Create middleware.
    """

    g_middleware(name)


command = group
