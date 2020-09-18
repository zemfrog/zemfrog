from zemfrog.decorators import auto_status_code
from zemfrog.helper import db_add, db_delete, db_update
from zemfrog.models import DefaultResponseSchema
from flask_apispec import marshal_with, use_kwargs
from extensions.sqlalchemy import db
from extensions.marshmallow import ma
from ${src_model} import ${name}
from ${src_schema} import ${name}Schema

class UpdateSchema(${name}Schema):
    __update__ = ma.Nested(${name}Schema)

schema = ${name}Schema()

@marshal_with(${name}Schema(many=True), 200)
def get():
    """
    Read all data.
    """

    data = ${name}.query.all()
    return data

@use_kwargs(schema)
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 403)
@auto_status_code
def add(**json):
    """
    Add data.
    """

    found = ${name}.query.filter_by(**json).first()
    if not found:
        model = ${name}(**json)
        db_add(db, model)
        status_code = 200
        reason = "Data berhasil ditambahkan."

    else:
        status_code = 403
        reason = "Data sudah ditemukan."

    return {
        "status_code": status_code,
        "reason": reason
    }

@use_kwargs(UpdateSchema)
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 404)
@marshal_with(DefaultResponseSchema, 403)
@auto_status_code
def update(**json):
    """
    Update data.
    """

    new_data = json.pop("__update__", None)
    if new_data and isinstance(new_data, dict):
        model = ${name}.query.filter_by(**json).first()
        if not model:
            status_code = 404
            reason = "Data tidak ditemukan."

        else:
            db_update(db, model, **new_data)
            status_code = 200
            reason = "Data berhasil diperbaharui."

    else:
        status_code = 403
        reason = "Data baru tidak ditemukan."

    return {
        "status_code": status_code,
        "reason": reason
    }

@use_kwargs(schema)
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 404)
@auto_status_code
def delete(**json):
    """
    Delete data.
    """

    model = ${name}.query.filter_by(**json).first()
    if model:
        db_delete(db, model)
        status_code = 200
        reason = "Data berhasil dihapus."

    else:
        status_code = 404
        reason = "Data tidak ditemukan."

    return {
        "status_code": status_code,
        "reason": reason
    }


docs = {"tags": ["${name}"]}
endpoint = "${url_prefix}"
url_prefix = "/${url_prefix}"
routes = [
    ("/get", get, ["GET"]),
    ("/add", add, ["POST"]),
    ("/update", update, ["PUT"]),
    ("/delete", delete, ["DELETE"])
]
