from flask import Blueprint
from flask.views import MethodView

class Resource(MethodView):
    url_route = None
    lowercase = True

class Api(Blueprint):
    def add_resource(self, resource: Resource):
        assert isinstance(resource, Resource)
        url = resource.url_route
        if not url:
            url = type(resource).__name__
            if resource.lowercase:
                url = url.lower()

        url = "/" + url.lstrip("/")
        self.add_url_rule(url, view_func=resource.as_view())
