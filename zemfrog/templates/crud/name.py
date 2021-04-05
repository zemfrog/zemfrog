from zemfrog.decorators import http_code, authenticate, marshal_with, use_kwargs
from zemfrog.helper import db_add, db_delete, db_update
from zemfrog.models import DefaultResponseSchema
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from {{ "" if main_app else ".." }}{{src_model}} import {{name}}

class Create{{name}}Schema(SQLAlchemyAutoSchema):
    class Meta:
        ordered = True
        model = {{name}}
        exclude = ("id",)

class Read{{name}}Schema(SQLAlchemyAutoSchema):
    class Meta:
        ordered = True
        model = {{name}}

class Update{{name}}Schema(SQLAlchemyAutoSchema):
    class Meta:
        ordered = True
        model = {{name}}
        exclude = ("id",)

# class Delete{{name}}Schema(SQLAlchemyAutoSchema):
#     class Meta:
#         ordered = True
#         model = {{name}}

class Limit{{name}}Schema(Schema):
    class Meta:
        ordered = True

    offset = fields.Integer()
    limit = fields.Integer()


@authenticate()
@use_kwargs(Limit{{name}}Schema(), location="query")
@marshal_with(200, Read{{name}}Schema(many=True))
def read(kwds):
    """
    Read all data.
    """

    offset = kwds.get("offset")
    limit = kwds.get("limit")
    data = {{name}}.query.offset(offset).limit(limit).all()
    return data

@authenticate()
@use_kwargs(Create{{name}}Schema())
@marshal_with(200, DefaultResponseSchema)
@marshal_with(403, DefaultResponseSchema)
@http_code
def create(kwds):
    """
    Add data.
    """

    found = {{name}}.query.filter_by(**kwds).first()
    if not found:
        model = {{name}}(**kwds)
        db_add(model)
        status_code = 200
        message = "Successfully added data."

    else:
        status_code = 403
        message = "Data already exists."

    return {
        "code": status_code,
        "message": message
    }

@authenticate()
@use_kwargs(Update{{name}}Schema())
@marshal_with(200, DefaultResponseSchema)
@marshal_with(404, DefaultResponseSchema)
@http_code
def update(kwds, id):
    """
    Update data.
    """

    model = {{name}}.query.get(id)
    if model:
        db_update(model, **kwds)
        status_code = 200
        message = "Successfully updating data."

    else:
        status_code = 404
        message = "Data not found."

    return {
        "code": status_code,
        "message": message
    }

@authenticate()
# @use_kwargs(Delete{{name}}Schema())
@marshal_with(200, DefaultResponseSchema)
@marshal_with(404, DefaultResponseSchema)
@http_code
def delete(id):
    """
    Delete data.
    """

    model = {{name}}.query.get(id)
    if model:
        db_delete(model)
        status_code = 200
        message = "Data deleted successfully."

    else:
        status_code = 404
        message = "Data not found."

    return {
        "code": status_code,
        "message": message
    }


tag = "{{ name }}"
description = "API"
url_prefix = "/{{url_prefix | lower}}"
routes = [
    ("/create", create, ["POST"]),
    ("/read", read, ["GET"]),
    ("/update/<id>", update, ["PUT"]),
    ("/delete/<id>", delete, ["DELETE"])
]
