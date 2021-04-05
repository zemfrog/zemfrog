from flask import jsonify


def get():
    return jsonify(text="welcome :')")


tag = "{{ name }}"
description = "API"
url_prefix = "/{{url_prefix | lower}}"
routes = [("/get", get, ["GET"])]
