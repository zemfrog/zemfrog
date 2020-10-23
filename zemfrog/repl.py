#!/usr/bin/env python
"""
Example of the fancy ZSH prompt that @anki-code was using.

The theme is coming from the xonsh plugin from the xhh project:
https://github.com/xxh/xxh-plugin-xonsh-theme-bar

See:
- https://github.com/xonsh/xonsh/issues/3356
- https://github.com/prompt-toolkit/python-prompt-toolkit/issues/1111
"""
import datetime
import os
import sys

from flask import Flask
from click import Group
from prompt_toolkit import prompt
from prompt_toolkit.application import get_app
from prompt_toolkit.formatted_text import (
    HTML,
    fragment_list_width,
    merge_formatted_text,
    to_formatted_text,
)
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.styles import Style

style = Style.from_dict(
    {
        "import_name": "#aaaaaa italic",
        "path": "#ffffff bold",
        "env": "bg:#666666",
        "left-part": "bg:#444444",
        "right-part": "bg:#444444",
        "padding": "bg:#444444",
    }
)


def get_prompt(app: Flask) -> HTML:
    """
    Build the prompt dynamically every time its rendered.
    """
    left_part = HTML(
        "<left-part>" " <import_name>%s</import_name> " "<path>%s</path>" "</left-part>"
    ) % (app.import_name, app.root_path)
    right_part = HTML(
        "<right-part> " " <env>%s</env> " " <time>%s</time> " "</right-part>"
    ) % (
        os.environ["ZEMFROG_ENV"],
        datetime.datetime.now().isoformat(),
    )

    used_width = sum(
        [
            fragment_list_width(to_formatted_text(left_part)),
            fragment_list_width(to_formatted_text(right_part)),
        ]
    )

    total_width = get_app().output.get_size().columns
    padding_size = total_width - used_width

    padding = HTML("<padding>%s</padding>") % (" " * padding_size,)

    return merge_formatted_text([left_part, padding, right_part, "\n", "$ "])


def get_commands(cli) -> dict:
    commands = {}
    for name, cmd in cli.commands.items():
        value = None
        if isinstance(cmd, Group):
            value = get_commands(cmd)
        commands[name] = value
    return commands


def get_auto_complete(cli) -> NestedCompleter:
    commands = {"flask": get_commands(cli)}
    completer = NestedCompleter.from_nested_dict(commands)
    return completer


def build_repl(app: Flask):
    while True:
        try:
            os.environ["FLASK_APP"] = app.import_name
            answer = prompt(
                lambda: get_prompt(app),
                style=style,
                completer=get_auto_complete(app.cli),
                refresh_interval=1,
            )
            os.system(answer)
        except (EOFError, KeyboardInterrupt):
            print("Bye bye!")
            sys.exit(1)
