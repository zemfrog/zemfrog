from zemfrog.api import Resource
from zemfrog.decorators import is_json_request, json_renderer

class ${name}Resource(Resource):
    name = "${name}".lower()
    decorators = [json_renderer, is_json_request]
