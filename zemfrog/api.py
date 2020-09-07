from flask import Blueprint
from flask.views import MethodView

class Resource(MethodView):
    name = None
    url_route = None

    @classmethod
    def get_name(cls):
        name = cls.name or cls.__name__
        return name

    @classmethod
    def get_url(cls):
        url = cls.url_route
        if not url:
            url = cls.get_name()

        url = "/" + url.lstrip("/")
        return url

    @classmethod
    def create(cls):
        name = cls.get_name()
        view = cls.as_view(name)
        return view

class Api(Blueprint):
    def add_resource(self, resource: Resource):
        assert issubclass(resource, Resource)
        url = resource.get_url()
        view = resource.create()
        self.add_url_rule(url, view_func=view)
