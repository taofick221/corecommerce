from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet

from core.throttles import ProductRateThrottle

from .filters import ProductFilter
from .models import Product
from .permissions import IsAdminOrReadOnly
from .serializers import ProductReadSerializer, ProductWriteSerializer
from .services import soft_delete_product


class ProductViewSet(ModelViewSet):

    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = ProductFilter
    search_fields = [
        "name",
        "description",
        "brand__name",
    ]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return (
            Product.objects.filter(
                is_active=True,
                deleted_at__isnull=True,
            )
            .select_related(
                "category",
                "brand",
            )
            .prefetch_related(
                "variants",
                "images",
            )
            .distinct()
        )

    def get_serializer_class(self):
        if self.action in [
            "list",
            "retrieve",
        ]:
            return ProductReadSerializer
        return ProductWriteSerializer

    def get_throttles(self):
        print(f"ACTION = {self.action}")

        if self.action in [
            "list",
            "retrieve",
        ]:
            print("USING PRODUCT THROTTLE")
            return [ProductRateThrottle()]

        print("USING DEFAULT THROTTLE")
        return super().get_throttles()

    def perform_destroy(self, instance):
        soft_delete_product(instance)
