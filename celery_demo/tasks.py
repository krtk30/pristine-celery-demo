import time
import random
import logging
from celery import shared_task

logger = logging.getLogger("celery_demo")


@shared_task(bind=True, max_retries=3, default_retry_delay=5, acks_late=True)
def slow_add(self, x, y):
    """
    Adds two numbers with retry simulation and logs lifecycle.
    """
    task_id = self.request.id
    logger.info(f"[{task_id}] Task slow_add received with x={x}, y={y}")
    try:
        time.sleep(2)
        if random.choice([True, False]):
            raise ValueError("Simulated random failure")
        result = x + y
        logger.info(f"[{task_id}] Task succeeded with result: {result}")
        return result
    except Exception as exc:
        logger.warning(f"[{task_id}] Task failed: {exc}. Retrying...")
        raise self.retry(exc=exc) from exc


@shared_task
def multiply(x):
    """
    Multiplies the result by 2.
    """
    logger.info(f"[multiply] Multiplying {x} by 2")
    return x * 2


@shared_task
def subtract(x):
    """
    Subtracts 5 from result.
    """
    logger.info(f"[subtract] Subtracting 5 from {x}")
    return x - 5