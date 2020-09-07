import click

from .generator import g_project

@click.group()
def main():
    """
    Zemfrog command line 
    """

@main.command("create")
@click.argument("name")
def create(name):
    """
    Create a project.
    """

    g_project(name)
