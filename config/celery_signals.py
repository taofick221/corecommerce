import logging

from celery.signals import task_failure, task_prerun, task_success

logger = logging.getLogger(__name__)


@task_prerun.connect
def task_started_handler(
    sender=None,
    task_id=None,
    task=None,
    **kwargs,
):
    logger.info(
        "Task started. task=%s task_id=%s",
        sender.name,
        task_id,
    )


@task_success.connect
def task_success_handler(sender=None, result=None, **kwargs):
    logger.info(
        "Task succeeded. task=%s result=%s",
        sender.name,
        result,
    )


@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, **kwargs):
    logger.error(
        "Task failed. task=%s task_id=%s error=%s",
        sender.name,
        task_id,
        exception,
    )
