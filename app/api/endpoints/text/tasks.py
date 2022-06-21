from typing import List

from app.core.celery import celery_app
from app.core.config import settings

from .utils import upload_file
from .services import save_stats, remove_text


@celery_app.task(queue=settings.CELERY_MAIN_QUEUE)
def upload_file_queue(path: str, content: str):
    upload_file(path=path, content=content)


def upload_file_task(path: str, content: str):
    if settings.CREATE_TASKS:
        upload_file_queue.delay(path=path, content=content)
    else:
        upload_file(path=path, content=content)


@celery_app.task(queue=settings.CELERY_MAIN_QUEUE)
def save_stats_queue(text_id: str, arguments: List[dict]):
    save_stats(text_id=text_id, arguments=arguments)


def save_stats_task(text_id: str, arguments: List[dict]):
    if settings.CREATE_TASKS:
        save_stats_queue.delay(text_id=text_id, arguments=arguments)
    else:
        save_stats(text_id=text_id, arguments=arguments)


@celery_app.task(queue=settings.CELERY_MAIN_QUEUE)
def remove_text_queue(text_id: str):
    remove_text(text_id=text_id)


def remove_text_task(text_id: str):
    if settings.CREATE_TASKS:
        remove_text_queue.delay(text_id=text_id)
    else:
        remove_text(text_id=text_id)
