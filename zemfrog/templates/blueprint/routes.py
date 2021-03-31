from flask import Blueprint

def init_blueprint():
    blueprint = Blueprint(
        "{{name}}",
        __name__,
        url_prefix="/{{name}}",
        static_folder="static",
        template_folder="templates",
    )
    return blueprint
