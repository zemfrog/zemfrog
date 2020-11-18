import re

from marshmallow.validate import Email
from marshmallow.exceptions import ValidationError


def validate_module_name(value: str, silently=False):
    re_var = re.compile(r"^([A-Za-z_]+[\w]+)$")
    if not re_var.search(value):
        if silently:
            return False
        raise SystemExit("Error: invalid name %r" % value)
    return True


def validate_email(value: str, silently=False):
    try:
        Email()(value)
    except ValidationError as e:
        if silently:
            return False
        raise SystemExit(e.messages[0])
    return True


def validate_username(value: str, silently=False):
    if not re.search(r"^([a-zA-Z]*)$", value):
        if silently:
            return False
        raise SystemExit("Name must be a character [a-zA-Z]")
    return True
