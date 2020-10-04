import click

from . import __version__
from .generator import g_project


@click.group()
@click.version_option(__version__, "-v", "--version", message="Zemfrog v%(version)s")
def main():
    """
    Zemfrog CLI
    """


@main.command("create")
@click.argument("name")
def create(name):
    """
    Create a project.
    """

    g_project(name)
