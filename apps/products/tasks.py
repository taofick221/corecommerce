import logging

from celery import shared_task

from .models import ProductVariant

logger = logging.getLogger(__name__)


@shared_task(queue="inventory")
def check_low_stock():
    low_stock_variants = ProductVariant.objects.filter(stock__lte=5).select_related(
        "product",
    )
    count = low_stock_variants.count()

    for variant in low_stock_variants:
        logger.warning(
            ("Low stock detected" "sku=%s" "stock=%s"),
            variant.sku,
            variant.stock,
        )
    logger.info(
        "Low stock check completed. count=%s",
        count,
    )

    return count
