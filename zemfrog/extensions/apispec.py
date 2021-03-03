"""
Reference: https://github.com/tiangolo/full-stack-flask-couchdb/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app/api/api_v1
"""

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask.app import Flask
from flask_apispec import FlaskApiSpec
from marshmallow import fields

FileField = fields.Raw


def init_app(app: Flask):
    global FileField

    docs = FlaskApiSpec(document_options=False)
    ma = MarshmallowPlugin()
    spec = APISpec(
        title=app.config.get("APISPEC_TITLE", "API Docs"),
        version=app.config.get("APISPEC_VERSION", "v1"),
        openapi_version=app.config.get("APISPEC_OAS_VERSION", "2.0"),
        plugins=[ma],
        securityDefinitions=app.config.get("APISPEC_SECURITY_DEFINITIONS", {}),
    )

    @ma.map_to_openapi_type("file", None)
    class FileField(fields.Raw):
        pass

    app.config.update({"APISPEC_SPEC": spec})
    docs.init_app(app)
    app.extensions["apispec"] = docs
