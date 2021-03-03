import re

from marshmallow.exceptions import ValidationError
from marshmallow.validate import Email


def validate_module_name(value: str, silently=False):
    re_var = re.compile(r"^([A-Za-z_]+[\w]+)$")
    if not re_var.search(value):
        if silently:
            return False
        raise ValidationError("Error: invalid name %r" % value)
    return True


def validate_email(value: str, silently=False):
    try:
        Email()(value)
    except ValidationError as e:
        if silently:
            return False
        raise ValidationError(e.messages[0])
    return True


def validate_username(value: str, silently=False):
    if not re.search(r"^([a-zA-Z]+)$", value):
        if silently:
            return False
        raise ValidationError("Name must be a character [a-zA-Z]")
    return True


def validate_password_length(value: str, silently=False):
    if len(value) < 8:
        if silently:
            return False
        raise ValidationError("Password length must be greater than or equal to 8")
    return True
