from rest_framework.exceptions import ValidationError
from uuid import uuid4
from django.db import transaction
from apps.orders.models import Order
from .models import Payment
from django.utils import timezone


def generate_transaction_id():

    return (
        f"TXN-{uuid4().hex[:12].upper()}"
    )

@transaction.atomic
def create_payment(user,order_id,provider):
    order=Order.objects.select_for_update().get(id=order_id,user=user)

    if Payment.objects.filter(order=order).exists():
        raise ValidationError({"payment":"Payment already exists"})
    
    if (order.payment_status==Order.PaymentStatus.PAID):
        raise ValidationError({"payment":"Order already paid"})
    
    if (order.status==Order.Status.CANCELLED):
        raise ValidationError({"order":"Cancelled order cannot be paid"})
    
    payment=Payment.objects.create(
        order=order,
        provider=provider,
        transaction_id=generate_transaction_id(),
        amount=order.total,
    )
    return payment

    
@transaction.atomic
def complete_payment(payment):
    if payment.status==Payment.Status.SUCCESS:
        return payment
    
    payment.status=Payment.Status.SUCCESS
    
    payment.paid_at=timezone.now()
    payment.save(
        update_fields=["status","paid_at"]
    )

    order=payment.order
    order.payment_status=(Order.PaymentStatus.PAID)
    order.save(update_fields=["payment_status"])
    return payment