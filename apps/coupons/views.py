from rest_framework import status

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .selectors import get_coupon_by_code
from .services import calculate_coupon_discount
from .serializers import ValidateCouponSerializer


class ValidateCouponView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ValidateCouponSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        coupon = get_coupon_by_code(
            serializer.validated_data["code"]
        )

        discount = calculate_coupon_discount(
            coupon=coupon,
            subtotal=serializer.validated_data[
                "subtotal"
            ],
        )

        return Response(
            {
                "coupon": coupon.code,
                "discount": discount,
            },
            status=status.HTTP_200_OK,
        )