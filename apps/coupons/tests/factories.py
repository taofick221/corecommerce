import factory
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

from apps.coupons.models import Coupon


class CouponFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Coupon

    code = factory.Sequence(
        lambda n: f"COUPON{n}"
    )

    discount_type = (
        Coupon.DiscountType.PERCENTAGE
    )

    discount_value = Decimal("10.00")

    minimum_order_amount = Decimal("100.00")

    maximum_discount_amount = Decimal("500.00")

    usage_limit = 100

    used_count = 0

    is_active = True

    valid_from = factory.LazyFunction(
        lambda: timezone.now() - timedelta(days=1)
    )

    valid_to = factory.LazyFunction(
        lambda: timezone.now() + timedelta(days=30)
    )