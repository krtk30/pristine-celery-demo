"""
Signals module for the HR app: handles post_save and m2m_changed signals.
"""

import logging

from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from .models import Employee
from .tasks import process_m2m_signal

logger = logging.getLogger("hr.signals")


@receiver(post_save, sender=Employee)
def log_employee_save(instance, created, **kwargs):
    """Log employee creation or update events."""
    action = "created" if created else "updated"
    logger.info("Employee %s (%s) was %s.", instance.name, instance.id, action)


@receiver(m2m_changed, sender=Employee.departments.through)
def enqueue_m2m_change_task(instance, action, pk_set, **kwargs):
    """Enqueue Celery task for employee department changes."""
    # Only after the change has been applied
    if action in ("post_add", "post_remove", "post_clear"):
        pk_list = list(pk_set) if pk_set is not None else []

        process_m2m_signal.delay(instance.id, action, pk_list)
        logger.debug(
            "Enqueued Celery task for Employee %s (%s) action=%s pks=%s",
            instance.name,
            instance.id,
            action,
            pk_list,
        )
