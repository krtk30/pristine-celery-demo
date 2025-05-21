"""
CeleryDemo app configuration module.
"""

from django.apps import AppConfig


class CeleryDemoConfig(AppConfig):
    """
    Configuration class for the celery_demo app.
        Sets the default auto field and the app name.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "celery_demo"
