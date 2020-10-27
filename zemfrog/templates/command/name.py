import click


@click.group("{{name}}")
def group():
    """
    {{name}} command.
    """


command = group
