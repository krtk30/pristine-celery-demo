"""
Celery task module for processing HR app many-to-many change signals asynchronously.
"""

import logging

from celery import shared_task

logger = logging.getLogger("hr.tasks")


@shared_task(bind=True, max_retries=3, default_retry_delay=5, acks_late=True)
def process_m2m_signal(self, instance_id: int, action: str, pk_list: list[int]) -> None:
    """
    Process a message sent from the m2m_changed signal.

    :param instance_id: The Employee PK
    :param action: one of 'post_add', 'post_remove', 'post_clear'
    :param pk_list: list of Department PKs added/removed
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
        # retry on failure
        raise self.retry(exc=exc) from exc
