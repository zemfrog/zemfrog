from marshmallow import Schema, fields


class DefaultResponseSchema(Schema):
    reason = fields.String()
    status_code = fields.Integer()


class LoginSuccessSchema(Schema):
    access_token = fields.String()


class LoginSchema(Schema):
    email = fields.Email()
    password = fields.String()


class RegisterSchema(LoginSchema):
    username = fields.String()


class RequestPasswordResetSchema(Schema):
    email = fields.Email()


class PasswordResetSchema(Schema):
    password = fields.String()