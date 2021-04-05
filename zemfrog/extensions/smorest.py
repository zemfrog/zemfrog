from flask_smorest import Api
from flask import Flask


def init_app(app: Flask):
    api = Api(app, spec_kwargs=app.config["API_SPEC_OPTIONS"])
    security_def = app.config["API_SECURITY_DEFINITIONS"]
    for scheme, attrs in security_def.items():
        api.spec.components.security_scheme(scheme, attrs)
