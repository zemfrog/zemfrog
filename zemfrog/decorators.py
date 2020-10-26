from functools import wraps
from typing import Callable
from flask import current_app
from flask_apispec import doc
from flask_jwt_extended import jwt_required


def auto_status_code(func: Callable) -> Callable:
    """
    Decorator to generate HTTP status response code automatically
    according to the key ``status_code`` in json.

    :param func: Your view function.

    """

    @wraps(func)
    def wrapper(*args, **kwds):
        result = func(*args, **kwds)
        status_code = 200
        if isinstance(result, dict):
            status_code = result.get("status_code", 200)

        if not isinstance(result, (tuple, list)):
            result = result, status_code

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


def authenticate(func: Callable) -> Callable:
    """
    Decorator to add jwt view authentication.
    Reference: https://github.com/tiangolo/full-stack-flask-couchdb/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app/api/api_v1.
    """

    func = api_doc(security=current_app.config.get("APISPEC_SECURITY_PARAMS", []))(
        jwt_required(func)
    )
    return func
