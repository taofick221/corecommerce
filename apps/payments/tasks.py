from celery import shared_task

@shared_task
def send_payment_email(payment_id):
    ...

@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def test_retry_task():
    raise Exception("Test Retry")




from celery import shared_task


@shared_task
def daily_report():
    print("Daily report task running") 