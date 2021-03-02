from functools import wraps
from typing import Callable

from flask import current_app, jsonify
from flask_apispec import doc
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


def api_doc(**kwds) -> Callable:
    """
    Decorator for adding API documentation through the documentation in the view function.
    """

    def wrapper(func: Callable):
        d = kwds.pop("description", func.__doc__ or "")
        kwds["description"] = d
        func = doc(**kwds)(func)
        return func

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
        func = api_doc(security=current_app.config.get("APISPEC_SECURITY_PARAMS", []))(
            jwt_required(roles)(func)
        )
        return func

    return decorated
