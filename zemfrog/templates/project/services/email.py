from extensions.celery import celery
from extensions.mail import mail
from flask_mail import Message


@celery.task
def send_email(*args, **kwds):
    msg = Message(*args, *kwds)
    mail.send(msg)
