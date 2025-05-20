import logging
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Employee

logger = logging.getLogger("hr.signals")

@receiver(post_save, sender=Employee)
def log_employee_save(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    logger.info(f"Employee {instance.name} ({instance.id}) was {action}.")

@receiver(m2m_changed, sender=Employee.departments.through)
def log_employee_department_change(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "post_add":
        logger.info(f"[m2m] Departments added to {instance.name} (IDs: {list(pk_set)})")
    elif action == "post_remove":
        logger.info(f"[m2m] Departments removed from {instance.name} (IDs: {list(pk_set)})")
    elif action == "post_clear":
        logger.info(f"[m2m] All departments cleared from {instance.name}")