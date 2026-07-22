from .models import Coupon


def get_coupon_by_code(code):

    return Coupon.objects.filter(
        code__iexact=code,
        is_active=True,
    ).first()
