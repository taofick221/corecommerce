from celery import shared_task


@shared_task
def send_payment_email(payment_id):
    print(f"Payment email sent for payment {payment_id}")