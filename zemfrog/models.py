from marshmallow import Schema, ValidationError, fields, validates

from .validators import validate_password_length, validate_username


class DefaultResponseSchema(Schema):
    message = fields.String()
    code = fields.Integer()


class LoginSuccessSchema(Schema):
    access_token = fields.String()


class LoginSchema(Schema):
    username = fields.Email(required=True)
    password = fields.String(required=True)
    grant_type = fields.String(default="password")


class RegisterSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    username = fields.Email(required=True)
    password = fields.String(required=True)

    @validates("first_name")
    def validate_first_name(self, value):
        if not validate_username(value, silently=True):
            raise ValidationError("First name must be a character [a-zA-Z]")

    @validates("last_name")
    def validate_last_name(self, value):
        if not validate_username(value, silently=True):
            raise ValidationError("Last name must be a character [a-zA-Z]")

    @validates("password")
    def validate_password(self, value):
        if not validate_password_length(value, silently=True):
            raise ValidationError("Password length must be greater than or equal to 8")


class RequestPasswordResetSchema(Schema):
    username = fields.Email(required=True)


class PasswordResetSchema(Schema):
    password = fields.String(required=True)

    @validates("password")
    def validate_password(self, value):
        if not validate_password_length(value, silently=True):
            raise ValidationError("Password length must be greater than or equal to 8")
