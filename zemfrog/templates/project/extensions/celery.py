from zemfrog.app import make_celery

celery = None


def init_app(app):
    global celery
    celery = make_celery(app)
