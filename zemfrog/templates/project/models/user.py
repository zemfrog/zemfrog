from zemfrog.globals import db
from zemfrog.mixins import (
    LogMixin,
    PermissionLinksMixin,
    PermissionMixin,
    RoleLinksMixin,
    RoleMixin,
    UserMixin,
)


class User(UserMixin, db.Model):
    pass


class Role(RoleMixin, db.Model):
    pass


class RoleLinks(RoleLinksMixin, db.Model):
    pass


class Permission(PermissionMixin, db.Model):
    pass


class PermissionLinks(PermissionLinksMixin, db.Model):
    pass


class Log(LogMixin, db.Model):
    pass
