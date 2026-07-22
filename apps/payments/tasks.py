import logging
from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.db.models import Sum
from django.utils import timezone

from apps.orders.models import Order

from .models import Payment

logger = logging.getLogger(__name__)


@shared_task(queue="reports")
def generate_daily_revenue_report():
    today = timezone.now().date()
    revenue = (
        Payment.objects.filter(
            status=Payment.Status.SUCCESS,
            paid_at__date=today,
        ).aggregate(total=Sum("amount"))["total"]
        or 0
    )

    logger.info("Daily revenue report generated. date=%s revenue=%s", today, revenue)
    return str(revenue)


@shared_task(queue="emails")
def send_payment_reminder():
    cutoff_time = timezone.now() - timedelta(minutes=30)

    payments = Payment.objects.select_related(
        "order",
        "order__user",
    ).filter(status=Payment.Status.PENDING, created_at__lt=cutoff_time)
    count = 0

    for payment in payments:
        logger.info(
            ("Payment reminder sent" "payment_id=%s" "order=%s" "user=%s"),
            payment.id,
            payment.order.order_number,
            payment.order.user.email,
        )
        count += 1
    logger.info("Payment reminder completed. count=%s", count)
    return count


@shared_task(
    queue="emails",
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=5,
)
def send_order_confirmation_email(order_id):
    order = Order.objects.select_related("user").get(id=order_id)

    send_mail(
        subject=f"Order {order.order_number} Confirmed",
        message=(
            f"Hello {order.full_name},\n\n"
            f"Your order has been placed successfully.\n"
            f"Order Number: {order.order_number}"
        ),
        from_email=None,
        recipient_list=[order.user.email],
        fail_silently=False,
    )
    logger.info(
        "Order confirmation email sent. order=%s",
        order.order_number,
    )
