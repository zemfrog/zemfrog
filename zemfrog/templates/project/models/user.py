from extensions.sqlalchemy import db
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship


class User(db.Model):
    """
    Simple user object.
    """

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    register_at = Column(DateTime)
    confirmed = Column(Boolean)
    confirmed_at = Column(DateTime)
    logs = relationship("Log")
    roles = relationship("Role")


class Role(db.Model):
    """
    Role user.
    """

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("user.id"))
    name = Column(String, nullable=False)


class Log(db.Model):
    """
    Log aktivitas user.
    """

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("user.id"))
    login_at = Column(DateTime)
    logout_at = Column(DateTime)
    request_password_reset_at = Column(DateTime)
    updated_at = Column(DateTime)
