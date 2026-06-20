from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from apps.orders.models import Order


@shared_task
def cancel_expired_orders():

    expired_time = timezone.now() - timedelta(hours=1)

    orders = Order.objects.filter(
        status=Order.Status.PENDING,
        created_at__lt=expired_time,
    )

    count = orders.update(
        status=Order.Status.CANCELLED
    )

    print(f"{count} orders cancelled")