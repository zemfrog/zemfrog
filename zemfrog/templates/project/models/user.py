from {{ "" if main_app else ".." }}extensions.sqlalchemy import db
from zemfrog.mixins import UserMixin, RoleMixin, PermissionMixin, LogMixin

class User(UserMixin, db.Model):
    pass


class Role(RoleMixin, db.Model):
    pass


class Permission(PermissionMixin, db.Model):
    pass


class Log(LogMixin, db.Model):
    pass
