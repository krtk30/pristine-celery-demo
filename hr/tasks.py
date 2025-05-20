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
        msg = f"[m2m][{action}] Employee ID {instance_id}: Dept IDs {pk_list}"
        logger.info(f"Processing signal task: {msg}")
    except Exception as exc:
        logger.error(f"Failed to process signal task: {exc}")
        # retry on failure
        raise self.retry(exc=exc) from exc