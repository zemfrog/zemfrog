import click
from flask import current_app
from flask.cli import with_appcontext

from ..loader import load_schemas

@click.group("schema")
def group():
    """
    Model schema generator.
    """

@group.command()
@with_appcontext
def load():
    """
    Memuat semua model schema secara otomatis.
    """

    load_schemas(current_app)


command = group
