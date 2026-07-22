from rest_framework import serializers

from .models import Coupon


class CouponSerializer(serializers.ModelSerializer):

    class Meta:

        model = Coupon

        fields = [
            "id",
            "code",
            "discount_type",
            "discount_value",
            "minimum_order_amount",
            "maximum_discount_amount",
            "usage_limit",
            "used_count",
            "is_active",
            "valid_from",
            "valid_to",
        ]


class ValidateCouponSerializer(serializers.Serializer):

    code = serializers.CharField(max_length=50)

    subtotal = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
