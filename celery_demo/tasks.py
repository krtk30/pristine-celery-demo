"""
Celery tasks module: defines asynchronous operations for addition, multiplication, and subtraction.
"""

import logging
import random
import time

from celery import shared_task

logger = logging.getLogger("celery_demo")


@shared_task(bind=True, max_retries=3, default_retry_delay=5, acks_late=True)
def slow_add(self, operand1, operand2):
    """
    Adds two numbers with retry simulation and logs lifecycle.
    """
    task_id = self.request.id
    logger.info(
        "[%s] Task slow_add received with x=%s, y=%s", task_id, operand1, operand2
    )
    try:
        time.sleep(2)
        if random.choice([True, False]):
            raise ValueError("Simulated random failure")
        result = operand1 + operand2
        logger.info("[%s] Task succeeded with result: %s", task_id, result)
        return result
    except Exception as exc:
        logger.warning("[%s] Task failed: %s. Retrying...", task_id, exc)
        raise self.retry(exc=exc) from exc


@shared_task
def multiply(value):
    """
    Multiplies the result by 2.
    """
    logger.info("Multiplying %s by 2", value)
    return value * 2


@shared_task
def subtract(value):
    """
    Subtracts 5 from result.
    """
    logger.info("Subtracting 5 from %s", value)
    return value - 5
