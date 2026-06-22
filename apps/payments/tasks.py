import logging
from django.utils import timezone
from celery import shared_task
from .models import Payment
from django.db.models import Sum
from datetime import timedelta

logger=logging.getLogger(__name__)

@shared_task
def generate_daily_revenue_report():
    today=timezone.now().date()
    revenue=(Payment.objects.filter(
        status=Payment.Status.SUCCESS,
        paid_at__date=today,
        ).aggregate(
            total=Sum("amount")
        )["total"]
        or 0
    )

    logger.info(
        "Daily revenue report generated. date=%s revenue=%s",
        today,
        revenue

    )
    return str(revenue)

@shared_task
def send_payment_reminder():
    cutoff_time=timezone.now()-timedelta(minutes=30)

    payments=(Payment.objects.select_related(
        "order",
        "order__user",
    ).prefetch_related(
        status=Payment.Status.PENDING,
        created_at__lt=cutoff_time
    ))
    count=0

    for payment in payments:
        logger.info(
            (
            "Payment reminder sent"
            "payment_id=%s"
            "order=%s"
            "user=%s"
            ),
            payment.id,
            payment.order.order_number,
            payment.order.user.email,
        )  
        count+=1
    logger.info(
        "Payment reminder completed. count=%s",
        count
    )
    return count