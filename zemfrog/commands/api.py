import click

from ..generator import g_api

@click.group("api")
def group():
    """
    API generator.
    """

@group.command()
@click.argument("name")
def new(name):
    """
    Create api ler.
    """

    g_api(name)

command = group
