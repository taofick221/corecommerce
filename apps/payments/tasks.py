from celery import shared_task
from django.core.mail import send_mail

from .models import Payment


@shared_task
def send_payment_email(payment_id):

    payment = Payment.objects.select_related(
        "order",
        "order__user"
    ).get(id=payment_id)

    send_mail(
        subject="Payment Successful",
        message=(
            f"Order: {payment.order.order_number}\n"
            f"Amount: {payment.amount}"
        ),
        from_email="noreply@corecommerce.com",
        recipient_list=[
            payment.order.user.email
        ],
    )