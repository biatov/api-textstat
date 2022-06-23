from celery import Celery

from app.core.config import settings

celery_app = Celery("worker")
celery_app.config_from_object(settings, namespace="CELERY")
celery_app.autodiscover_tasks(packages=(
    "app.api.endpoints.text",
))
