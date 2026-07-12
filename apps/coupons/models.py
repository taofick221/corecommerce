from decimal import Decimal

from django.db import models
from django.utils import timezone


class Coupon(models.Model):

    class DiscountType(models.TextChoices):
        PERCENTAGE = "percentage", "Percentage"
        FIXED = "fixed", "Fixed"

    code = models.CharField(
        max_length=50,
        unique=True,
    )

    discount_type = models.CharField(
        max_length=20,
        choices=DiscountType.choices,
    )

    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    minimum_order_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    maximum_discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    usage_limit = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    used_count = models.PositiveIntegerField(
        default=0,
    )

    is_active = models.BooleanField(
        default=True,
    )

    valid_from = models.DateTimeField()

    valid_to = models.DateTimeField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.code

    @property
    def is_valid(self):

        now = timezone.now()

        if not self.is_active:
            return False

        if now < self.valid_from:
            return False

        if now > self.valid_to:
            return False

        if (
            self.usage_limit is not None
            and
            self.used_count >= self.usage_limit
        ):
            return False

        return True