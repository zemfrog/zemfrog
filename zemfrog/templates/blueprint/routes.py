from flask import Blueprint
from . import views

blueprint = Blueprint("${name}", __name__, url_prefix="/${name}", static_folder="static", template_folder="templates")
