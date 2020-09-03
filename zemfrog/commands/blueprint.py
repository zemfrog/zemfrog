import click

from ..generator import g_blueprint

@click.group("blueprint")
def group():
    """
    Blueprint generator.
    """

@group.command()
@click.argument("name")
def new(name):
    """
    Create blueprint ler.
    """

    g_blueprint(name)

command = group
