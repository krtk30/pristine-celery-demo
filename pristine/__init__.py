"""
Pristine project Celery application initializer.
"""

from .celery import app as celery_app

__all__ = ["celery_app"]
