import logging
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Employee
from .tasks import process_m2m_signal

logger = logging.getLogger("hr.signals")

@receiver(post_save, sender=Employee)
def log_employee_save(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    logger.info(f"Employee {instance.name} ({instance.id}) was {action}.")

@receiver(m2m_changed, sender=Employee.departments.through)
def enqueue_m2m_change_task(sender, instance, action, pk_set, **kwargs):
    # Only after the change has been applied
    if action in ("post_add", "post_remove", "post_clear"):
        pk_list = list(pk_set) if pk_set is not None else []

        process_m2m_signal.delay(instance.id, action, pk_list)
        logger.debug(
            f"Enqueued Celery task for Employee {instance.name} ({instance.id}) action={action} pks={pk_list}"
        )