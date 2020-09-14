from flask import Blueprint

blueprint = Blueprint("auth", __name__, url_prefix="/auth/jwt")
