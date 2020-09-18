from flask import request, jsonify
from functools import wraps
from .exception import ZemfrogJSONError


def is_json_request(func):
    """
    Decorator untuk memastikan json request.
    """

    @wraps(func)
    def wrapper(*args, **kwds):
        json = request.json
        if not json and request.method != "GET":
            return jsonify(status_code=403, reason="Bukan json request!")
        return func(*args, **kwds)

    return wrapper


def json_renderer(func):
    """
    Decorator untuk membuat response json.
    """

    @wraps(func)
    def wrapper(*args, **kwds):
        result = func(*args, **kwds)
        if not isinstance(result, (dict, list)):
            raise ZemfrogJSONError("%r harus tipe dict atau list" % result)

        status_code = result.get("status_code", 200)
        return jsonify(result), status_code

    return wrapper


def auto_status_code(func):
    """
    Decorator untuk membuat response status kode HTTP secara otomatis
    sesuai key ``status_code`` pada json.
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
