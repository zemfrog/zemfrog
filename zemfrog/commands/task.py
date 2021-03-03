import click
from flask.cli import with_appcontext

from ..generator import g_task


@click.group("task")
def group():
    """
    Task generator.
    """


@group.command()
@with_appcontext
@click.argument("name")
def new(name):
    """
    Create task.
    """

    g_task(name)


command = group
