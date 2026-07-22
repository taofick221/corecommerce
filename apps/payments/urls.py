from django.urls import path

from .views import CreatePaymentView, PaymentDetailView, PaymentListView

urlpatterns = [
    path(
        "",
        PaymentListView.as_view(),
        name="payments",
    ),
    path(
        "<int:payment_id>/",
        PaymentDetailView.as_view(),
        name="payment_detail",
    ),
    path(
        "create/<int:order_id>/",
        CreatePaymentView.as_view(),
        name="create_payment",
    ),
]
