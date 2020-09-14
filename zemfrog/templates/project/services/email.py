from extensions.celery import celery
from flask_mail import Message


@celery.task
def send_email(msg, **kwds):
    mail = Message(**kwds)
    mail.send(msg)
