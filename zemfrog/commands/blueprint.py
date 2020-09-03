import click

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

command = group
