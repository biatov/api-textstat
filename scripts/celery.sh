#! /usr/bin/env bash
set -e

/usr/local/bin/celery -A app.core worker -l info -Q "${CELERY_MAIN_QUEUE}" -c 1
