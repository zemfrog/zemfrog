import click
from flask.cli import with_appcontext

from ..generator import g_blueprint


@click.group("blueprint")
def group():
    """
    Blueprint generator.
    """


@group.command()
@with_appcontext
@click.argument("name")
def new(name):
    """
    Create blueprint.
    """

    g_blueprint(name)


command = group
