from django.test import TestCase

from .factories import (
    CategoryFactory,
    BrandFactory,
)

from apps.products.serializers import (
    ProductVariantSerializer,
    ProductImageSerializer,
    ProductWriteSerializer,
)


class ProductVariantSerializerTest(TestCase):

    def test_valid_variant(self):
        serializer = ProductVariantSerializer(
            data={
                "size": "42",
                "color": "Black",
                "price": 100,
                "stock": 10,
                "sku": "SKU100",
                "is_default": True,
            }
        )

        self.assertTrue(
            serializer.is_valid()
        )

    def test_negative_price(self):
        serializer = ProductVariantSerializer(
            data={
                "size": "42",
                "color": "Black",
                "price": -100,
                "stock": 10,
                "sku": "SKU100",
                "is_default": True,
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

    def test_negative_stock(self):
        serializer = ProductVariantSerializer(
            data={
                "size": "42",
                "color": "Black",
                "price": 100,
                "stock": -1,
                "sku": "SKU100",
                "is_default": True,
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

class ProductImageSerializerTest(TestCase):

    def test_valid_image(self):
        serializer = ProductImageSerializer(
            data={
                "alt_text": "Front",
                "order": 0,
                "is_primary": True,
            }
        )

        self.assertTrue(
            serializer.is_valid()
        )

    def test_negative_order(self):
        serializer = ProductImageSerializer(
            data={
                "alt_text": "Front",
                "order": -1,
                "is_primary": True,
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )


class ProductWriteSerializerTest(TestCase):

    def setUp(self):
        self.category = CategoryFactory()
        self.brand = BrandFactory()

    def get_payload(self):
        return {
            "name": "Nike",
            "description": "Running Shoe",
            "category": self.category.id,
            "brand": self.brand.id,
            "is_active": True,
            "variants": [
                {
                    "size": "42",
                    "color": "Black",
                    "price": 100,
                    "stock": 10,
                    "sku": "SKU100",
                    "is_default": True,
                }
            ],
            "images": [
                {
                    "alt_text": "Front",
                    "order": 0,
                    "is_primary": True,
                }
            ],
        }

    def test_valid_payload(self):
        serializer = ProductWriteSerializer(
            data=self.get_payload()
        )

        self.assertTrue(
            serializer.is_valid()
        )

    def test_without_variant(self):
        payload = self.get_payload()

        payload["variants"] = []

        serializer = ProductWriteSerializer(
            data=payload
        )

        self.assertFalse(
            serializer.is_valid()
        )

    def test_duplicate_sku(self):
        payload = self.get_payload()

        payload["variants"] = [
            {
                "size": "42",
                "color": "Black",
                "price": 100,
                "stock": 10,
                "sku": "SKU100",
                "is_default": True,
            },
            {
                "size": "43",
                "color": "White",
                "price": 120,
                "stock": 5,
                "sku": "SKU100",
                "is_default": False,
            },
        ]

        serializer = ProductWriteSerializer(
            data=payload,
        )

        self.assertFalse(
            serializer.is_valid(),
        )

    def test_duplicate_variant(self):
        payload = self.get_payload()

        payload["variants"] = [
            {
                "size": "42",
                "color": "Black",
                "price": 100,
                "stock": 10,
                "sku": "SKU100",
                "is_default": True,
            },
            {
                "size": "42",
                "color": "Black",
                "price": 120,
                "stock": 5,
                "sku": "SKU200",
                "is_default": False,
            },
        ]

        serializer = ProductWriteSerializer(
            data=payload,
        )

        self.assertFalse(
            serializer.is_valid(),
        )

    def test_multiple_default_variant(self):
        payload = self.get_payload()

        payload["variants"] = [
            {
                "size": "42",
                "color": "Black",
                "price": 100,
                "stock": 10,
                "sku": "SKU100",
                "is_default": True,
            },
            {
                "size": "43",
                "color": "White",
                "price": 120,
                "stock": 5,
                "sku": "SKU200",
                "is_default": True,
            },
        ]

        serializer = ProductWriteSerializer(
            data=payload,
        )

        self.assertFalse(
            serializer.is_valid(),
        )

    def test_empty_size(self):
        payload = self.get_payload()

        payload["variants"][0]["size"] = ""

        serializer = ProductWriteSerializer(
            data=payload,
        )

        self.assertFalse(
            serializer.is_valid(),
        )

    def test_empty_color(self):
        payload = self.get_payload()

        payload["variants"][0]["color"] = ""

        serializer = ProductWriteSerializer(
            data=payload,
        )

        self.assertFalse(
            serializer.is_valid(),
        )

    def test_empty_sku(self):
        payload = self.get_payload()

        payload["variants"][0]["sku"] = ""

        serializer = ProductWriteSerializer(
            data=payload,
        )

        self.assertFalse(
            serializer.is_valid(),
        )