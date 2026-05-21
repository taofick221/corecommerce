from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.orders.models import Order
from .models import Payment
from .serializers import PaymentSerializer,CreatePaymentSerializer
from .services import create_payment,complete_payment
from rest_framework.response import Response
from .selectors import get_user_payments


class CreatePaymentView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request,order_id):
        serializer=CreatePaymentSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        payment=create_payment(
            user=request.user,
            order_id=order_id,
            provider=serializer.validated_data["provider"]
        )
        response_serializer=PaymentSerializer(payment)
        return Response(response_serializer.data,status=status.HTTP_201_CREATED)


class PaymentListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        payments = get_user_payments(request.user)
        serializer = PaymentSerializer(payments,many=True,)

        return Response(serializer.data,status=status.HTTP_200_OK,)


class PaymentDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request,payment_id,):

        payment = get_object_or_404(
            get_user_payments(request.user),id=payment_id,)

        serializer = PaymentSerializer(payment)

        return Response(serializer.data,status=status.HTTP_200_OK,)

