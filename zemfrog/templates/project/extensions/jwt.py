from flask import jsonify
from flask_jwt_extended import JWTManager
from {{ "" if main_app else ".." }}models.user import User

jwt = JWTManager()


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    user = User.query.filter_by(email=identity).first()
    return user


@jwt.user_loader_error_loader
def custom_user_loader_error(identity):
    ret = {"reason": "User {} not found".format(identity), "status_code": 404}
    return jsonify(ret), 404


init_app = jwt.init_app
