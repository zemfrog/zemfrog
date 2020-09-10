import click
from ..generator import g_command

@click.group("command")
def group():
    """
    Command generator.
    """


@group.command()
@click.argument("name")
def new(name):
    """
    Create command.
    """

    g_command(name)

command = group
