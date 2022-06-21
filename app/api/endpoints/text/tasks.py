from app.core.celery import celery_app
from app.core.config import settings

from .utils import upload_file


@celery_app.task(queue=settings.CELERY_MAIN_QUEUE)
def upload_file_queue(path: str, content: str):
    upload_file(path=path, content=content)


def upload_file_task(path: str, content: str):
    if settings.CREATE_TASKS:
        upload_file_queue.delay(path=path, content=content)
    else:
        upload_file(path=path, content=content)
