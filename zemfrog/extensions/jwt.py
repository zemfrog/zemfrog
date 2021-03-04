from flask import Flask, jsonify
from flask_jwt_extended import JWTManager

from ..helper import get_object_model


def init_app(app: Flask):
    User = get_object_model("user")
    jwt = JWTManager()

    @jwt.user_loader_callback_loader
    def user_loader_callback(identity):
        user = User.query.filter_by(email=identity).first()
        if user and not user.confirmed:
            user = None

        return user

    @jwt.user_loader_error_loader
    def custom_user_loader_error(identity):
        ret = {"reason": "User {} not found".format(identity), "status_code": 404}
        return jsonify(ret), 404

    jwt.init_app(app)
