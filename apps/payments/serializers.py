from rest_framework import serializers

from .models import Payment


class CreatePaymentSerializer(serializers.Serializer):

    provider = serializers.ChoiceField(choices=Payment.Provider.choices)


class PaymentSerializer(serializers.ModelSerializer):

    order_id = serializers.IntegerField(
        source="order.id",
        read_only=True,
    )

    order_number = serializers.CharField(
        source="order.order_number",
        read_only=True,
    )

    class Meta:

        model = Payment

        fields = [
            "id",
            "order_id",
            "order_number",
            "provider",
            "status",
            "transaction_id",
            "amount",
            "paid_at",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "status",
            "transaction_id",
            "amount",
            "paid_at",
            "created_at",
        ]
