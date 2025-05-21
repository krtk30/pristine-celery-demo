# M2M Change Signals

This module uses Django’s `m2m_changed` signal on the `Employee.departments` relationship to asynchronously process and log all adds, removes, and clears via a Celery task.

## Celery Task

The `process_m2m_signal` task lives in `hr/tasks.py` and handles the message:

```python
from celery import shared_task
import logging

logger = logging.getLogger("hr.tasks")

@shared_task(bind=True, max_retries=3, default_retry_delay=5, acks_late=True)
def process_m2m_signal(self, instance_id: int, action: str, pk_list: list[int]) -> None:
    """
    Process and log the M2M signal event asynchronously.

    :param instance_id: Employee primary key
    :param action: e.g. 'post_add', 'post_remove', 'post_clear', 'post_save_created'
    :param pk_list: list of affected Department PKs
    """
    try:
        logger.info(
            "Processing signal task: [m2m][%s] Employee ID %s: Dept IDs %s",
            action,
            instance_id,
            pk_list,
        )
    except Exception as exc:
        logger.error("Failed to process signal task: %s", exc)
        raise self.retry(exc=exc)
```

## Logging & Monitoring

- **Celery**: The task is executed by Celery workers:
  ```bash
  poetry run celery -A pristine worker --loglevel=info
  ```
- **Flower**: Monitor live tasks via Flower:
  ```bash
  poetry run celery -A pristine flower --port=5555
  ```
- **Worker logs**: Uses lazy logging to defer string interpolation (W1203 compliance).

## File Location

- **Signals**: `hr/signals.py`
- **Celery Task**: `hr/tasks.py`

---
