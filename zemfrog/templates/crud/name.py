from zemfrog.decorators import auto_status_code, authenticate
from zemfrog.helper import db_add, db_delete, db_update
from zemfrog.models import DefaultResponseSchema
from flask_apispec import marshal_with, use_kwargs
from {{ "" if main_app else ".." }}extensions.marshmallow import ma
from {{ "" if main_app else ".." }}{{src_model}} import {{name}}

class Create{{name}}Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = {{name}}

class Read{{name}}Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = {{name}}

class Update{{name}}Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = {{name}}

    __update__ = ma.Nested(Read{{name}}Schema(strict=True))

class Delete{{name}}Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = {{name}}

@authenticate()
@marshal_with(Read{{name}}Schema(many=True), 200)
def get():
    """
    Read all data.
    """

    data = {{name}}.query.all()
    return data

@authenticate()
@use_kwargs(Create{{name}}Schema(strict=True))
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 403)
@auto_status_code
def add(**json):
    """
    Add data.
    """

    found = {{name}}.query.filter_by(**json).first()
    if not found:
        model = {{name}}(**json)
        db_add(model)
        status_code = 200
        reason = "Successfully added data."

    else:
        status_code = 403
        reason = "Data already exists."

    return {
        "status_code": status_code,
        "reason": reason
    }

@authenticate()
@use_kwargs(Update{{name}}Schema(strict=True))
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
        model = {{name}}.query.filter_by(**json).first()
        if not model:
            status_code = 404
            reason = "Data not found."

        else:
            db_update(model, **new_data)
            status_code = 200
            reason = "Successfully updating data."

    else:
        status_code = 403
        reason = "New data not found."

    return {
        "status_code": status_code,
        "reason": reason
    }

@authenticate()
@use_kwargs(Delete{{name}}Schema(strict=True))
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 404)
@auto_status_code
def delete(**json):
    """
    Delete data.
    """

    model = {{name}}.query.filter_by(**json).first()
    if model:
        db_delete(model)
        status_code = 200
        reason = "Data deleted successfully."

    else:
        status_code = 404
        reason = "Data not found."

    return {
        "status_code": status_code,
        "reason": reason
    }


docs = {"tags": ["{{name}}"]}
endpoint = "{{url_prefix}}"
url_prefix = "/{{url_prefix}}"
routes = [
    ("/get", get, ["GET"]),
    ("/add", add, ["POST"]),
    ("/update", update, ["PUT"]),
    ("/delete", delete, ["DELETE"])
]
