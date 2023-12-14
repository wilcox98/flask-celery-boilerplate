from celery import shared_task
import celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


class MyTask(celery.Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print("{0!r} failed: {1!r}".format(task_id, exc))


@shared_task(name="hello", base=MyTask)
def hello():
    print("hello")

    logger.info("Hello logger")
    return {"msg": "hello"}
