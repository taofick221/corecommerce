from decimal import Decimal

from rest_framework.exceptions import ValidationError

from .models import Coupon


def calculate_coupon_discount(
    coupon,
    subtotal,
):

    if not coupon:
        raise ValidationError({
            "coupon":
            "Coupon not found"
        })

    if not coupon.is_valid:
        raise ValidationError({
            "coupon":
            "Coupon expired or inactive"
        })

    if subtotal < coupon.minimum_order_amount:

        raise ValidationError({
            "coupon":
            (
                f"Minimum order amount is "
                f"{coupon.minimum_order_amount}"
            )
        })

    discount = Decimal("0.00")

    if (
        coupon.discount_type
        == Coupon.DiscountType.PERCENTAGE
    ):

        discount = (
            subtotal
            * coupon.discount_value
        ) / Decimal("100")

        if (
            coupon.maximum_discount_amount
            and
            discount > coupon.maximum_discount_amount
        ):
            discount = (
                coupon.maximum_discount_amount
            )

    else:

        discount = (
            coupon.discount_value
        )

    if discount > subtotal:
        discount = subtotal

    return discount