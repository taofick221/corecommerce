import logging
import csv
from datetime import timedelta
from django.db import transaction
from django.utils import timezone
from celery import shared_task
from .models import Order

logger=logging.getLogger(__name__)

@shared_task
@transaction.atomic
def cancel_expired_orders():
    expiry_time=timezone.now()-timedelta(hours=1)
    orders=Order.objects.select_for_update().filter(
        status=Order.Status.PENDING,
        payment_status=Order.PaymentStatus.PENDING,
        created_at__lt=expiry_time,
    ).prefetch_related(
        "items",
        "items__variant",
    )
    cancelled_count=0

    for order in orders:
        for item in order.items.all():
            variant=item.variant
            variant.stock+=item.quantity
            variant.save(update_fields=["stock"])
        
        order.status=Order.Status.CANCELLED
        order.save(update_fields=["status"])
        cancelled_count+=1
        logger.info(
            "Order cancelled. order_number=%s",order.order_number,
        )
    logger.info(
        "Expired order cancellation completed. count=%s",
        cancelled_count
    )
    return cancelled_count

@shared_task
def  export_orders_csv():
    orders=Order.objects.select_related("user")
    filename="/tmp/orders.csv"
    with open(
        filename,
        "w",
        newline="",
    ) as file:
        writer=csv.writer(file)
        writer.writerow([
            "Order_Number",
            "User",
            "Total",
            "Status",
        ])
        for order in orders:
            writer.writerow([
                order.order_number,
                order.user.email,
                order.total,
                order.status,
            ])
    logger.info(
        "Orders exported. count=%s",
        orders.count(),
    )
    return filename