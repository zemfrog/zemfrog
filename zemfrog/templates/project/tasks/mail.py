from zemfrog.globals import celery, mail


@celery.task
def send_email(*args, **kwds):
    mail.send_message(*args, **kwds)
