from {{ "" if main_app else ".." }}extensions.celery import celery
from {{ "" if main_app else ".." }}extensions.mail import mail


@celery.task
def send_email(*args, **kwds):
    mail.send_message(*args, **kwds)
