from functools import wraps
from typing import Callable

from flask import current_app, jsonify
from flask_smorest import Blueprint
from flask_smorest.arguments import ArgumentsMixin
from flask_smorest.response import ResponseMixin
from flask_smorest.pagination import PaginationMixin
from flask_smorest.etag import EtagMixin
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.utils import get_jwt_claims


def http_code(func: Callable) -> Callable:
    """
    Decorator to generate HTTP status response code automatically
    according to the key ``code`` in json.

    :param func: Your view function.

    """

    @wraps(func)
    def wrapper(*args, **kwds):
        result = func(*args, **kwds)
        code = 200
        if isinstance(result, dict):
            code = result.get("code", 200)

        if not isinstance(result, (tuple, list)):
            result = result, code

        return result

    return wrapper


def api_doc(*args, **kwds) -> Callable:
    """
    See here https://flask-smorest.readthedocs.io/en/latest/api_reference.html#flask_smorest.Blueprint.doc
    """

    wrapper = Blueprint.doc(*args, **kwds)
    return wrapper


def use_kwargs(*args, **kwds) -> Callable:
    """
    See here https://flask-smorest.readthedocs.io/en/latest/arguments.html
    """

    wrapper = ArgumentsMixin().arguments(*args, **kwds)
    return wrapper


def marshal_with(*args, **kwds) -> Callable:
    """
    See here https://flask-smorest.readthedocs.io/en/latest/response.html#
    """

    wrapper = ResponseMixin().alt_response(*args, **kwds)
    return wrapper


def paginate(*args, **kwds) -> Callable:
    """
    See here https://flask-smorest.readthedocs.io/en/latest/pagination.html.
    """

    wrapper = PaginationMixin().paginate(*args, **kwds)
    return wrapper


def etag(schema=None) -> Callable:
    """
    See here https://flask-smorest.readthedocs.io/en/latest/etag.html
    """

    wrapper = EtagMixin().etag(schema)
    return wrapper


def jwt_required(roles={}) -> Callable:
    """
    Decorator to protect views with JWT & user roles.
    """

    def decorated(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwds):
            verify_jwt_in_request()
            claims = get_jwt_claims()
            jwt_roles = claims.get("roles", {})
            for role, permissions in roles.items():
                if not isinstance(permissions, (list, tuple)):
                    permissions = []

                if role in jwt_roles:
                    valid_perms = jwt_roles.get(role, [])
                    for perm in permissions:
                        if perm not in valid_perms:
                            return (
                                jsonify(message="You don't have permission!", code=403),
                                403,
                            )
                else:
                    return (jsonify(message="Role not allowed!", code=403), 403)

            return func(*args, **kwds)

        return wrapper

    return decorated


def authenticate(roles={}) -> Callable:
    """
    Decorator to add jwt view authentication to API Docs.
    Reference: https://github.com/tiangolo/full-stack-flask-couchdb/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app/api/api_v1.
    """

    def decorated(func: Callable) -> Callable:
        func = api_doc(security=current_app.config.get("API_SECURITY_PARAMS", []))(
            jwt_required(roles)(func)
        )
        return func

    return decorated
