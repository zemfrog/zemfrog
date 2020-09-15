from extensions.celery import celery
from extensions.mail import mail


@celery.task
def send_email(*args, **kwds):
    mail.send_message(*args, **kwds)
