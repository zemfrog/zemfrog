import os
from typing import Dict, List

import click
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from ..helper import import_attr
from ..repl import build_repl


def loader(app: Flask):
    """
    Load all applications and combine them together using ``DispatcherMiddleware``.
    """

    apps: List[Dict] = app.config.get("APPS", [])
    mounts = {}
    for a in apps:
        if not isinstance(a, dict):
            a = {"name": a}

        name = a["name"]
        path = a.get("path", "/" + name)
        help = a.get("help", "")
        yourapp: Flask = import_attr(name + ".wsgi.app")

        @click.command(name, context_settings=dict(ignore_unknown_options=True))
        @click.option("-r", "--repl", is_flag=True, help="Activates REPL mode.")
        @click.argument("args", nargs=-1, type=click.UNPROCESSED)
        def cli(repl, args):
            os.environ["FLASK_APP"] = yourapp.import_name
            if repl:
                build_repl(yourapp)
            else:
                os.system("flask " + " ".join(args))

        cli.help = help
        app.cli.add_command(cli)
        mounts[path] = yourapp

    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, mounts)
