from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from core.throttles import LoginRateThrottle, RegisterRateThrottle

from .serializers import CustomTokenSerializer, UserSerializer


class RegisterView(APIView):
    throttle_classes = [RegisterRateThrottle]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer
    throttle_classes = [LoginRateThrottle]
