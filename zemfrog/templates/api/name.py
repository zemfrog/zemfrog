from flask_apispec import marshal_with


@marshal_with(None, 200)
def get():
    return {"text": "welcome :')"}


docs = {"tags": ["${name}"]}
endpoint = "${url_prefix}"
url_prefix = "/${url_prefix}"
routes = [("/get", get, ["GET"])]
