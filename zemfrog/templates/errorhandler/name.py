from flask import jsonify
from werkzeug.exceptions import HTTPException


def handler(error: HTTPException):
    code = error.code
    return jsonify(message="error occurred %r" % error.description, code=code), code
