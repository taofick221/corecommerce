from .models import Payment


def get_user_payments(user):
    return Payment.objects.select_related("order", "order__user").filter(
        order__user=user
    )
