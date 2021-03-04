import click
from flask.cli import with_appcontext

from ..generator import g_filter


@click.group("filter")
def group():
    """
    Jinja filter generator.
    """


@group.command()
@with_appcontext
@click.argument("name")
def new(name):
    """
    Create a new filter.
    """

    g_filter(name)


command = group
