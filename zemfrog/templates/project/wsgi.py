from zemfrog.app import create_app, make_celery

app = create_app(__name__)
celery = make_celery(app)
