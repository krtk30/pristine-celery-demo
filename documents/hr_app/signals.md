# M2M Change Signals

We use Django’s `m2m_changed` on `Employee.departments` to log every add/remove/clear.

## Signal Handler

```python
@receiver(m2m_changed, sender=Employee.departments.through)
def log_employee_department_change(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        logger.info(f"[m2m] Added to {instance.name}: Dept IDs {list(pk_set)}")
    elif action == "post_remove":
        logger.info(f"[m2m] Removed from {instance.name}: Dept IDs {list(pk_set)}")
    elif action == "post_clear":
        logger.info(f"[m2m] Cleared all from {instance.name}")
```

---
## Log File
	•	Location: pristine/logs/hr.log
	•	Rotation: via RotatingFileHandler (1 MB max, 5 backups)
	•	Format: [YYYY-MM-DD HH:MM:SS] [LEVEL] [hr.signals] message

---






