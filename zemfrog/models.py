from marshmallow import Schema, fields, validates, ValidationError
from .validators import validate_username


class DefaultResponseSchema(Schema):
    reason = fields.String()
    status_code = fields.Integer()


class LoginSuccessSchema(Schema):
    access_token = fields.String()


class LoginSchema(Schema):
    username = fields.Email(required=True)
    password = fields.String(required=True)


class RegisterSchema(LoginSchema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)

    @validates("first_name")
    def validate_first_name(self, value):
        if not validate_username(value, silently=True):
            raise ValidationError("First name must be a character [a-zA-Z]")

    @validates("last_name")
    def validate_last_name(self, value):
        if not validate_username(value, silently=True):
            raise ValidationError("Last name must be a character [a-zA-Z]")


class RequestPasswordResetSchema(Schema):
    username = fields.Email(required=True)


class PasswordResetSchema(Schema):
    password = fields.String(required=True)