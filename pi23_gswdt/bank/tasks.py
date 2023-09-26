from celery.utils.log import get_task_logger
from django.conf import settings
from django_redis_task_lock import lock

from config.celery_app import app

LOGGER = get_task_logger(__name__)


@app.task(name="task__test_celery")
@lock(debug=settings.DEBUG)
def task__test_celery(*args, **kwargs):
    LOGGER.info("Executing the task with args: [%s] and kwargs: [%s]", args, kwargs)
    return f"Executing the task with args: [{args}] and kwargs: [{kwargs}]"
