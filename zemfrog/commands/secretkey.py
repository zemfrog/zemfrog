import os

import click


@click.group("secretkey")
def group():
    """
    Secret key generator.
    """


@group.command()
@click.argument("length", type=int)
def new(length):
    """
    Generate a random secret key.
    """

    print(os.urandom(length).hex())


command = group
