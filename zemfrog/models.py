from marshmallow import Schema, fields


class DefaultResponseSchema(Schema):
    reason = fields.String()
    status_code = fields.Integer()


class LoginSuccessSchema(Schema):
    access_token = fields.String()


class LoginSchema(Schema):
    email = fields.String()
    password = fields.String()


class RegisterSchema(LoginSchema):
    username = fields.String()


class RequestPasswordResetSchema(Schema):
    email = fields.String()


class PasswordResetSchema(Schema):
    password = fields.String()