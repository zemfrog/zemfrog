from datetime import datetime, timedelta
from flask import url_for
from flask_jwt_extended import create_access_token, decode_token
from flask_apispec import use_kwargs, marshal_with
from jwt import DecodeError, ExpiredSignatureError
from werkzeug.security import generate_password_hash, check_password_hash
from zemfrog.decorators import auto_status_code
from zemfrog.helper import db_add, db_update, db_commit, get_mail_template, get_user_roles
from zemfrog.models import (
    DefaultResponseSchema,
    LoginSchema,
    LoginSuccessSchema,
    PasswordResetSchema,
    RegisterSchema,
    RequestPasswordResetSchema,
)

from {{ "" if main_app else ".." }}models.user import User, Log
from {{ "" if main_app else ".." }}tasks.email import send_email


@use_kwargs(LoginSchema(strict=True), location="form")
@marshal_with(DefaultResponseSchema, 404)
@marshal_with(LoginSuccessSchema, 200)
@auto_status_code
def login(**kwds):
    """
    Login and get access token.
    """

    email = kwds.get("username")
    passw = kwds.get("password")
    user = User.query.filter_by(email=email).first()

    if user and user.confirmed and check_password_hash(user.password, passw):
        login_at = datetime.utcnow()
        log = Log(login_at=login_at)
        user.logs.append(log)
        db_commit()
        roles = get_user_roles(user)
        claims = {"roles": roles}
        access_token = create_access_token(email, user_claims=claims)
        return {"access_token": access_token}

    return {"reason": "Incorrect email or password.", "status_code": 404}


@use_kwargs(RegisterSchema(strict=True), location="form")
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 403)
@auto_status_code
def register(**kwds):
    """
    Register an account.
    """

    email = kwds.get("username")
    passw = kwds.get("password")
    first_name = kwds.get("first_name")
    last_name = kwds.get("last_name")
    username = first_name + " " + last_name
    if email:
        user = User.query.filter_by(email=email).first()
        if not user:
            if username and passw:
                passw = generate_password_hash(passw)
                user = User(
                    first_name=first_name,
                    last_name=last_name,
                    name=username,
                    email=email,
                    password=passw,
                    register_at=datetime.utcnow(),
                )
                db_add(user)
                token = create_access_token(
                    email,
                    expires_delta=False,
                    user_claims={"token_registration": True},
                )
                link_confirm = url_for(".confirm_account", token=token)
                msg = get_mail_template("register.html", link_confirm=link_confirm)
                send_email.delay("Registration", html=msg, recipients=[email])
                reason = "Successful registration."
                status_code = 200
            else:
                reason = "Username and password are required."
                status_code = 403
        else:
            reason = "Email already exists."
            status_code = 403
    else:
        reason = "Email required."
        status_code = 403

    return {"reason": reason, "status_code": status_code}


@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 403)
@auto_status_code
def confirm_account(token):
    """
    Confirm account.
    """

    try:
        data = decode_token(token)
        email = data["identity"]
        if not data["user_claims"].get("token_registration"):
            raise DecodeError

        user = User.query.filter_by(email=email).first()
        if user and not user.confirmed:
            reason = "Confirmed."
            status_code = 200
            db_update(user, confirmed=True, confirmed_at=datetime.utcnow())

        else:
            raise DecodeError

    except DecodeError:
        reason = "Invalid token."
        status_code = 403

    return {"reason": reason, "status_code": status_code}


@use_kwargs(RequestPasswordResetSchema(strict=True), location="form")
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 404)
@marshal_with(DefaultResponseSchema, 403)
@auto_status_code
def request_password_reset(**kwds):
    """
    Request a password reset.
    """

    email = kwds.get("username")
    if email:
        user = User.query.filter_by(email=email).first()
        if not user:
            reason = "User not found."
            status_code = 404
        else:
            reason = "A password reset request has been sent."
            status_code = 200
            token = create_access_token(
                email,
                expires_delta=timedelta(hours=2),
                user_claims={"token_password_reset": True},
            )
            link_reset = url_for(".password_reset", token=token)
            msg = get_mail_template(
                "request_password_reset.html", link_reset=link_reset
            )
            send_email.delay("Forgot password", html=msg, recipients=[email])
            log = Log(request_password_reset_at=datetime.utcnow())
            user.logs.append(log)
            db_commit()
    else:
        reason = "Email required."
        status_code = 403

    return {"reason": reason, "status_code": status_code}


@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 401)
@marshal_with(DefaultResponseSchema, 403)
@auto_status_code
def confirm_password_reset_token(token):
    """
    Validate password reset token.
    """

    try:
        data = decode_token(token)
        email = data["identity"]
        if not data["user_claims"].get("token_password_reset"):
            raise DecodeError

        user = User.query.filter_by(email=email).first()
        if user:
            reason = "Valid token."
            status_code = 200
        else:
            raise DecodeError

    except DecodeError:
        reason = "Invalid token."
        status_code = 401

    except ExpiredSignatureError:
        reason = "Token expired."
        status_code = 403

    return {"reason": reason, "status_code": status_code}


@use_kwargs(PasswordResetSchema(strict=True), location="form")
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 403)
@marshal_with(DefaultResponseSchema, 401)
@marshal_with(DefaultResponseSchema, 404)
@auto_status_code
def password_reset(token, **kwds):
    """
    Reset user password.
    """

    try:
        data = decode_token(token)
        email = data["identity"]
        if not data["user_claims"].get("token_password_reset"):
            raise DecodeError

        user = User.query.filter_by(email=email).first()
        passw = kwds.get("password")
        if user and passw:
            passw = generate_password_hash(passw)
            log = Log(updated_at=datetime.utcnow())
            user.logs.append(log)
            db_update(user, password=passw)
            reason = "Successfully change password."
            status_code = 200
        else:
            reason = "User not found."
            status_code = 404

    except DecodeError:
        reason = "Invalid token."
        status_code = 401

    except ExpiredSignatureError:
        reason = "Token expired."
        status_code = 403

    return {"reason": reason, "status_code": status_code}
