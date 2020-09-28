import click
from flask.cli import with_appcontext
from ..generator import g_api, g_api_crud


@click.group("api")
def group():
    """
    API generator.
    """


@group.command()
@with_appcontext
@click.argument("name")
@click.option("--crud", is_flag=True, help="Create a REST API based on the ORM model.")
def new(name, crud):
    """
    Create REST API.
    """

    func = g_api
    if crud:
        func = g_api_crud
    func(name)


command = group
