from flask import jsonify


def get():
    return jsonify(text="welcome :')")


docs = {"tags": ["{{name}}"]}
endpoint = "{{url_prefix | lower}}"
url_prefix = "/{{url_prefix | lower}}"
routes = [("/get", get, ["GET"])]
