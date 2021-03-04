import click
from flask.cli import with_appcontext

from ..generator import g_model


@click.group("model")
def group():
    """
    Model generator.
    """


@group.command()
@with_appcontext
@click.argument("name")
def new(name):
    """
    Create model.
    """

    g_model(name)


command = group
