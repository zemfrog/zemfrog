from flask import jsonify


def handler(error):
    """
    Reference: https://webargs.readthedocs.io/en/latest/framework_support.html#error-handling
    """

    headers = error.data.get("headers", None)
    messages = error.data.get("messages", ["Invalid request."])
    if headers:
        return jsonify({"errors": messages}), error.code, headers
    else:
        return jsonify({"errors": messages}), error.code
