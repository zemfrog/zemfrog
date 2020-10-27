from flask import jsonify


def get():
    return jsonify(text="welcome :')")


docs = {"tags": ["{{name}}"]}
endpoint = "{{url_prefix}}"
url_prefix = "/{{url_prefix}}"
routes = [("/get", get, ["GET"])]
