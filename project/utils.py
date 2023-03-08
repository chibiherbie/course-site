import json
from celery import Celery


def get_task_file(lesson):
    """Возвращает нужный файл с задачами"""
    with open(f'project/tasks/tasks_{lesson}.json', encoding='utf-8') as f:
        file = json.load(f)
    return file


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        # broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    # celery = Celery(app.import_name, broker='pyamqp://guest@localhost//')
    # # celery.conf.update(app.config['CELERY_CONFIG'])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
