from flask import Flask
from flask_mail import Mail


def init_app(app: Flask):
    mail = Mail()
    mail.init_app(app)
