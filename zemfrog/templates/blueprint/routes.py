from flask import Blueprint

blueprint = Blueprint(
    "${name}",
    __name__,
    url_prefix="/${name}",
    static_folder="static",
    template_folder="templates",
)
