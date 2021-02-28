from flask_mail import Mail
from flask import Flask

def init_app(app: Flask):
    mail = Mail()
    mail.init_app(app)
