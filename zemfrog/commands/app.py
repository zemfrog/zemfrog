import click

from ..generator import g_project


@click.group("app")
def group():
    """
    App generator.
    """


@group.command()
@click.argument("name")
def new(name):
    """
    Create a new app.
    """

    g_project(name, name + ".wsgi")


command = group
