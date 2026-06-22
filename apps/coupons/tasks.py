import logging
from django.utils import timezone
from celery import shared_task
from .models import Coupon

logger=logging.getLogger(__name__)

@shared_task
def disable_expired_coupons():
    expired_coupons=Coupon.objects.filter(
        is_active=True,
        valid_to__lt=timezone.now()
    )
    count=expired_coupons.update(
        is_active=False,
    )
    logger.info(
        "Expired coupons disabled. count=%s",
        count,
    )
    return count
