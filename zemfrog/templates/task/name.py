from {{ "" if main_app else ".." }}extensions.celery import celery

@celery.task
def {{task_name}}():
    pass
