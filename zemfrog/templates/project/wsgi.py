from zemfrog.app import create_app, make_celery

app = create_app("{{import_name}}")
celery = make_celery(app)
