from datetime import datetime, timedelta
from flask import request, url_for
from flask_jwt_extended import create_access_token, decode_token
from flask_apispec import use_kwargs, marshal_with
from jwt import DecodeError, ExpiredSignatureError
from werkzeug.security import generate_password_hash, check_password_hash
from zemfrog.decorators import auto_status_code
from zemfrog.helper import db_add, db_update, db_commit, get_mail_template
from zemfrog.models import (
    DefaultResponseSchema,
    LoginSchema,
    LoginSuccessSchema,
    PasswordResetSchema,
    RegisterSchema,
    RequestPasswordResetSchema,
)

from extensions.sqlalchemy import db
from models.user import User, Log
from services.email import send_email


@use_kwargs(LoginSchema)
@marshal_with(DefaultResponseSchema, 401)
@marshal_with(LoginSuccessSchema, 200)
@auto_status_code
def login(**kwds):
    email = kwds.get("email")
    passw = kwds.get("password")
    user = User.query.filter_by(email=email).first()

    if user and user.confirmed and check_password_hash(user.password, passw):
        login_at = datetime.utcnow()
        log = Log(login_at=login_at)
        user.logs.append(log)
        db_commit(db)
        access_token = create_access_token(email)
        return {"access_token": access_token}

    return {"reason": "Email atau password salah.", "status_code": 401}


@use_kwargs(RegisterSchema)
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 403)
@marshal_with(DefaultResponseSchema, 401)
@auto_status_code
def register(**kwds):
    username = kwds.get("username")
    passw = kwds.get("password")
    email = kwds.get("email")
    if email:
        user = User.query.filter_by(email=email).first()
        if not user:
            if username and passw:
                passw = generate_password_hash(passw)
                user = User(
                    name=username,
                    email=email,
                    password=passw,
                    register_at=datetime.utcnow(),
                )
                db_add(db, user)
                token = create_access_token(
                    email,
                    expires_delta=False,
                    user_claims={"token_registration": True},
                )
                link_confirm = url_for(".confirm_account", token=token)
                msg = get_mail_template("register.html", link_confirm=link_confirm)
                send_email.delay("Pendaftaran", html=msg, recipients=[email])
                reason = "Sukses daftar"
                status_code = 200
            else:
                reason = "Username dan password dibutuhkan"
                status_code = 403
        else:
            reason = "Email telah digunakan."
            status_code = 403
    else:
        reason = "Email dibutuhkan."
        status_code = 401

    return {"reason": reason, "status_code": status_code}


@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 403)
@auto_status_code
def confirm_account(token):
    try:
        data = decode_token(token)
        email = data["identity"]
        if not data["user_claims"].get("token_registration"):
            raise DecodeError

        user = User.query.filter_by(email=email).first()
        if user:
            if not user.confirmed:
                reason = "Terkonfirmasi."
                status_code = 200
                db_update(db, user, confirmed=True, confirmed_at=datetime.utcnow())
            else:
                raise DecodeError

        else:
            raise DecodeError

    except DecodeError:
        reason = "Invalid token."
        status_code = 403

    return {"reason": reason, "status_code": status_code}


@use_kwargs(RequestPasswordResetSchema)
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 403)
@marshal_with(DefaultResponseSchema, 401)
@auto_status_code
def request_password_reset(**kwds):
    email = kwds.get("email")
    if email:
        user = User.query.filter_by(email=email).first()
        if not user:
            reason = "Email tidak terdaftar."
            status_code = 403
        else:
            reason = "Permintaan password reset terkirim."
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
    else:
        reason = "Email dibutuhkan."
        status_code = 401

    return {"reason": reason, "status_code": status_code}


@use_kwargs(PasswordResetSchema)
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 403)
@marshal_with(DefaultResponseSchema, 401)
@marshal_with(DefaultResponseSchema, 404)
@auto_status_code
def password_reset(token, **kwds):
    try:
        data = decode_token(token)
        email = data["identity"]
        if not data["user_claims"].get("token_password_reset"):
            raise DecodeError

        user = User.query.filter_by(email=email).first()
        passw = kwds.get("password")
        if user and passw:
            passw = generate_password_hash(passw)
            db_update(db, user, password=passw)
            reason = "Sukses password reset."
            status_code = 200
        else:
            reason = "User tidak ditemukan"
            status_code = 404

    except DecodeError:
        reason = "Invalid token."
        status_code = 401

    except ExpiredSignatureError:
        reason = "Token kadaluwarsa."
        status_code = 403

    return {"reason": reason, "status_code": status_code}
