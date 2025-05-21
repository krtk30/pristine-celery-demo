"""
Celery application configuration for the Pristine Django project.
"""

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pristine.settings")

app = Celery("pristine")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
