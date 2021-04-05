from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType

from .exception import ZemfrogRoleNotFound, ZemfrogRolePermissionNotFound
from .helper import db_commit, db_update


class UserMixin:
    """
    User model.
    """

    id = Column(Integer, primary_key=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(EmailType, nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    registration_date = Column(DateTime)
    confirmed = Column(Boolean, default=False)
    date_confirmed = Column(DateTime)

    @declared_attr
    def logs(cls):
        return relationship("Log")

    @declared_attr
    def roles(cls):
        return relationship("Role", secondary="role_links", lazy="dynamic")

    def get_role(self, name, silently=False):
        for role in self.roles:
            if role.name == name:
                return role

        if silently:
            return False

        raise ZemfrogRoleNotFound

    def has_role(self, name):
        try:
            self.get_role(name)
        except ZemfrogRoleNotFound:
            return False
        else:
            return True

    def add_role(self, role):
        have = self.get_role(role.name, silently=True)
        if not have:
            self.roles.append(role)
            db_commit()
            return True
        return False

    def delete_role(self, name):
        role = self.get_role(name, silently=True)
        if role:
            self.roles.remove(role)
            db_commit()
            return True
        return False

    def update_role(self, name, **kwds):
        role = self.get_role(name, silently=True)
        if role:
            db_update(role, **kwds)
            return True
        return False


class RoleMixin:
    """
    Role user.
    """

    id = Column(Integer, primary_key=True)

    @declared_attr
    def user_id(cls):
        return Column(ForeignKey("user.id"))

    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(255), nullable=False)

    @declared_attr
    def permissions(cls):
        return relationship("Permission", secondary="permission_links", lazy="dynamic")

    def get_perm(self, name, silently=False):
        for perm in self.permissions:
            if perm.name == name:
                return perm

        if silently:
            return False

        raise ZemfrogRolePermissionNotFound

    def has_perm(self, name):
        try:
            self.get_perm(name)
        except ZemfrogRolePermissionNotFound:
            return False
        else:
            return True

    def add_perm(self, perm):
        have = self.get_perm(perm.name, silently=True)
        if not have:
            self.permissions.append(perm)
            db_commit()
            return True
        return False

    def delete_perm(self, name):
        perm = self.get_perm(name, silently=True)
        if perm:
            self.permissions.remove(perm)
            db_commit()
            return True
        return False

    def update_perm(self, name, **kwds):
        perm = self.get_perm(name, silently=True)
        if perm:
            db_update(perm, **kwds)
            return True
        return False


class PermissionMixin:
    """
    Role permission.
    """

    id = Column(Integer, primary_key=True)

    @declared_attr
    def role_id(cls):
        return Column(ForeignKey("role.id"))

    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(255), nullable=False)


class LogMixin:
    """
    User activity log.
    """

    id = Column(Integer, primary_key=True)

    @declared_attr
    def user_id(cls):
        return Column(ForeignKey("user.id"))

    login_date = Column(DateTime)
    date_requested_password_reset = Column(DateTime)
    date_set_new_password = Column(DateTime)


class RoleLinksMixin:
    id = Column(Integer, primary_key=True)

    @declared_attr
    def user_id(cls):
        return Column(ForeignKey("user.id"))

    @declared_attr
    def role_id(cls):
        return Column(ForeignKey("role.id"))


class PermissionLinksMixin:
    id = Column(Integer, primary_key=True)

    @declared_attr
    def role_id(cls):
        return Column(ForeignKey("role.id"))

    @declared_attr
    def permission_id(cls):
        return Column(ForeignKey("permission.id"))
