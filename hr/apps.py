# pylint: disable=import-outside-toplevel
"""AppConfig for the HR app; initializes signals and tasks."""
from django.apps import AppConfig


class HrConfig(AppConfig):
    """Django AppConfig for the HR application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "hr"

    def ready(self):
        import hr.signals  # noqa  # pylint: disable=unused-import
        import hr.tasks  # noqa  # pylint: disable=unused-import
