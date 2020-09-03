import click
import os

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

    print("creating %r project..." % name)
    g_project(name)
