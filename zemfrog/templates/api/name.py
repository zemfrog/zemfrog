from zemfrog.decorators import json_renderer

@json_renderer
def get():
    return {
        "text": "welcome :')"
    }


endpoint = "${url_prefix}"
url_prefix = "/${url_prefix}"
routes = [
    ("/get", get, ["GET"])
]
