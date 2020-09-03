import click

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

command = group
