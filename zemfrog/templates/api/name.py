from flask import jsonify
from zemfrog.models import DefaultResponseSchema
from zemfrog.decorators import marshal_with, http_code


@marshal_with(200, DefaultResponseSchema)
@http_code
def get():
    code = 200
    message = "What's up?"
    return {"code": code, "message": message}


tag = "{{ name }}"
description = "API"
url_prefix = "/{{url_prefix | lower}}"
routes = [("/get", get, ["GET"])]
