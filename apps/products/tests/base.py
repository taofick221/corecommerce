from django.urls import reverse

from rest_framework.test import APITestCase

from .factories import (
    AdminFactory,
    UserFactory,
    ProductFactory,
    ProductVariantFactory,
    ProductImageFactory,
)


class BaseProductTestCase(APITestCase):

    def setUp(self):

        self.admin = AdminFactory()

        self.user = UserFactory()

        self.product = ProductFactory()

        self.variant = ProductVariantFactory(
            product=self.product,
        )

        self.image = ProductImageFactory(
            product=self.product,
        )

        self.list_url = reverse(
            "products-list",
        )

        self.detail_url = reverse(
            "products-detail",
            kwargs={
                "slug": self.product.slug,
            },
        )