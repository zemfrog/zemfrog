from flask import request, jsonify

def is_json_request(func):
    def wrapper(*args, **kwds):
        json = request.json
        if not json and request.method != "GET":
            return jsonify(status_code=403, reason="Bukan json request!")
        return func(*args, **kwds)
    return wrapper

def json_renderer(func):
    def wrapper(*args, **kwds):
        result = func(*args, **kwds)
        return jsonify(result)
    return wrapper
