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
    Menambahkn dokumentasi API melalui dokumentasi yang ada di fungsi view.
    """

    def wrapper(func: Callable):
        d = kwds.pop("description", func.__doc__ or "")
        kwds["description"] = d
        func = doc(**kwds)(func)
        return func

    return wrapper


def authenticate(func: Callable) -> Callable:
    """
    Autentikasi view dengan jwt.
    """

    func = api_doc(security=current_app.config.get("APISPEC_SECURITY_PARAMS", []))(
        jwt_required(func)
    )
    return func
