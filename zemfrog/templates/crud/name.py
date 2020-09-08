from zemfrog.decorators import is_json_request, json_renderer
from zemfrog.helper import db_add, db_delete, db_update
from flask import request
from extensions.sqlalchemy import db
from ${src_model} import ${name}
from ${src_schema} import ${name}Schema

schema = ${name}Schema()

@json_renderer
def get():
    """
    Read all data.
    """

    data = ${name}.query.all()
    return schema.dump(data, many=True)

@is_json_request
@json_renderer
def add():
    """
    Add data.
    """

    json = request.get_json()
    found = ${name}.query.filter_by(**json).first()
    if not found:
        model = schema.load(json)
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

@is_json_request
@json_renderer
def update():
    """
    Update data.
    """

    json = request.get_json()
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

@is_json_request
@json_renderer
def delete():
    """
    Delete data.
    """

    json = request.get_json()
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

endpoint = "${url_prefix}"
url_prefix = "/${url_prefix}"
routes = [
    ("/get", get, ["GET"]),
    ("/add", add, ["POST"]),
    ("/update", update, ["PUT"]),
    ("/delete", delete, ["DELETE"])
]
