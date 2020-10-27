from flask import jsonify
from werkzeug.exceptions import HTTPException


def handler(error: HTTPException):
    return jsonify(message="error occurred %r" % error.description), error.code
