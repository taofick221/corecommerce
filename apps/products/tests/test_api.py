import uuid

from django.utils import timezone
from rest_framework import status

from .base import BaseProductTestCase


class ProductListAPITest(BaseProductTestCase):

    def test_product_list_success(self):
        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            1,
        )

    def test_product_list_contains_product(self):
        response = self.client.get(self.list_url)

        self.assertEqual(
            response.data["results"][0]["name"],
            self.product.name,
        )

    def test_product_list_returns_slug(self):
        response = self.client.get(self.list_url)

        self.assertEqual(
            response.data["results"][0]["slug"],
            self.product.slug,
        )

    def test_product_list_returns_category(self):
        response = self.client.get(self.list_url)

        self.assertEqual(
            response.data["results"][0]["category"],
            self.product.category.id,
        )

    def test_product_list_returns_brand(self):
        response = self.client.get(self.list_url)

        self.assertEqual(
            response.data["results"][0]["brand"],
            self.product.brand.id,
        )

    def test_soft_deleted_product_not_visible(self):
        self.product.deleted_at = timezone.now()
        self.product.save()

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.data["count"],
            0,
        )

        self.assertEqual(
            len(response.data["results"]),
            0,
        )

    def test_inactive_product_not_visible(self):
        self.product.is_active = False
        self.product.save()

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.data["count"],
            0,
        )

        self.assertEqual(
            len(response.data["results"]),
            0,
        )

    def test_list_response_contains_variants(self):
        response = self.client.get(self.list_url)

        self.assertIn(
            "variants",
            response.data["results"][0],
        )

    def test_list_response_contains_images(self):
        response = self.client.get(self.list_url)

        self.assertIn(
            "images",
            response.data["results"][0],
        )

    def test_list_response_is_success(self):
        response = self.client.get(self.list_url)

        self.assertTrue(
            status.is_success(response.status_code),
        )


class ProductDetailAPITest(BaseProductTestCase):

    def test_product_detail_success(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_product_detail_returns_correct_product(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(
            response.data["slug"],
            self.product.slug,
        )

    def test_product_detail_returns_name(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(
            response.data["name"],
            self.product.name,
        )

    def test_product_detail_returns_variants(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(
            len(response.data["variants"]),
            1,
        )

    def test_product_detail_returns_images(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(
            len(response.data["images"]),
            1,
        )

    def test_invalid_slug_returns_404(self):
        response = self.client.get(
            "/api/products/not-found/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_deleted_product_returns_404(self):
        self.product.deleted_at = timezone.now()
        self.product.save()

        response = self.client.get(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_inactive_product_returns_404(self):
        self.product.is_active = False
        self.product.save()

        response = self.client.get(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )


class ProductCreateAPITest(BaseProductTestCase):

    def setUp(self):
        super().setUp()

        self.payload = {
            "name": "Nike Air Max",
            "description": "Running Shoe",
            "category": self.product.category.id,
            "brand": self.product.brand.id,
            "is_active": True,
            "variants": [
                {
                    "size": "42",
                    "color": "Black",
                    "price": "120.00",
                    "stock": 10,
                    "sku": f"SKU-{uuid.uuid4().hex[:8].upper()}",
                    "is_default": True,
                }
            ],
            "images": [
                {
                    "alt_text": "Front Image",
                    "order": 0,
                    "is_primary": True,
                }
            ],
        }

    def test_admin_can_create_product(self):
        self.client.force_authenticate(self.admin)

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_user_cannot_create_product(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_anonymous_cannot_create_product(self):
        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_product_created_successfully(self):
        self.client.force_authenticate(self.admin)

        self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            self.product.__class__.objects.count(),
            2,
        )

    def test_create_without_variants(self):
        self.client.force_authenticate(self.admin)

        self.payload["variants"] = []

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_duplicate_sku_validation(self):
        self.client.force_authenticate(self.admin)

        self.payload["variants"] = [
            {
                "size": "42",
                "color": "Black",
                "price": "100",
                "stock": 10,
                "sku": "DUPLICATE",
                "is_default": True,
            },
            {
                "size": "43",
                "color": "White",
                "price": "120",
                "stock": 20,
                "sku": "DUPLICATE",
                "is_default": False,
            },
        ]

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_duplicate_variant_validation(self):
        self.client.force_authenticate(self.admin)

        unique_sku = f"SKU-{uuid.uuid4().hex[:8].upper()}"

        self.payload["variants"] = [
            {
                "size": "42",
                "color": "Black",
                "price": "100",
                "stock": 10,
                "sku": unique_sku,
                "is_default": True,
            },
            {
                "size": "42",
                "color": "Black",
                "price": "120",
                "stock": 20,
                "sku": f"SKU-{uuid.uuid4().hex[:8].upper()}",
                "is_default": False,
            },
        ]

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_multiple_default_variant_validation(self):
        self.client.force_authenticate(self.admin)

        self.payload["variants"] = [
            {
                "size": "42",
                "color": "Black",
                "price": "100",
                "stock": 10,
                "sku": f"SKU-{uuid.uuid4().hex[:8].upper()}",
                "is_default": True,
            },
            {
                "size": "43",
                "color": "White",
                "price": "120",
                "stock": 20,
                "sku": f"SKU-{uuid.uuid4().hex[:8].upper()}",
                "is_default": True,
            },
        ]

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_invalid_price(self):
        self.client.force_authenticate(self.admin)

        self.payload["variants"][0]["price"] = -100

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_invalid_stock(self):
        self.client.force_authenticate(self.admin)

        self.payload["variants"][0]["stock"] = -10

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_create_returns_created_product(self):
        self.client.force_authenticate(self.admin)

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.data["name"],
            "Nike Air Max",
        )

        self.assertEqual(
            response.data["description"],
            "Running Shoe",
        )


class ProductUpdateAPITest(BaseProductTestCase):

    def setUp(self):
        super().setUp()

        self.payload = {
            "name": "Updated Product",
            "description": "Updated Description",
            "category": self.product.category.id,
            "brand": self.product.brand.id,
            "is_active": True,
            "variants": [
                {
                    "id": self.variant.id,
                    "size": "43",
                    "color": "White",
                    "price": "200.00",
                    "stock": 15,
                    "sku": self.variant.sku,
                    "is_default": True,
                }
            ],
            "images": [
                {
                    "id": self.image.id,
                    "alt_text": "Updated Image",
                    "order": 0,
                    "is_primary": True,
                }
            ],
        }

    def test_admin_can_update_product(self):
        self.client.force_authenticate(self.admin)

        response = self.client.put(
            self.detail_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_user_cannot_update_product(self):
        self.client.force_authenticate(self.user)

        response = self.client.put(
            self.detail_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_anonymous_cannot_update_product(self):
        response = self.client.put(
            self.detail_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_product_name_updated(self):
        self.client.force_authenticate(self.admin)

        self.client.put(
            self.detail_url,
            self.payload,
            format="json",
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.name,
            "Updated Product",
        )

    def test_product_description_updated(self):
        self.client.force_authenticate(self.admin)

        self.client.put(
            self.detail_url,
            self.payload,
            format="json",
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.description,
            "Updated Description",
        )

    def test_variant_updated(self):
        self.client.force_authenticate(self.admin)

        self.client.put(
            self.detail_url,
            self.payload,
            format="json",
        )

        self.variant.refresh_from_db()

        self.assertEqual(
            self.variant.size,
            "43",
        )

        self.assertEqual(
            self.variant.color,
            "white",
        )

        self.assertEqual(
            self.variant.stock,
            15,
        )

    def test_image_updated(self):
        self.client.force_authenticate(self.admin)

        self.client.put(
            self.detail_url,
            self.payload,
            format="json",
        )

        self.image.refresh_from_db()

        self.assertEqual(
            self.image.alt_text,
            "Updated Image",
        )

    def test_update_invalid_price(self):
        self.client.force_authenticate(self.admin)

        self.payload["variants"][0]["price"] = -1

        response = self.client.put(
            self.detail_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_update_invalid_stock(self):
        self.client.force_authenticate(self.admin)

        self.payload["variants"][0]["stock"] = -10

        response = self.client.put(
            self.detail_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_update_duplicate_sku(self):
        self.client.force_authenticate(self.admin)

        self.payload["variants"] = [
            {
                "id": self.variant.id,
                "size": "43",
                "color": "White",
                "price": "200.00",
                "stock": 15,
                "sku": "DUPLICATE",
                "is_default": True,
            },
            {
                "size": "44",
                "color": "Black",
                "price": "300.00",
                "stock": 5,
                "sku": "DUPLICATE",
                "is_default": False,
            },
        ]

        response = self.client.put(
            self.detail_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_update_duplicate_variant(self):
        self.client.force_authenticate(self.admin)

        self.payload["variants"] = [
            {
                "id": self.variant.id,
                "size": "43",
                "color": "White",
                "price": "200.00",
                "stock": 15,
                "sku": self.variant.sku,
                "is_default": True,
            },
            {
                "size": "43",
                "color": "White",
                "price": "300.00",
                "stock": 5,
                "sku": "SKU-NEW",
                "is_default": False,
            },
        ]

        response = self.client.put(
            self.detail_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_update_without_default_variant(self):
        self.client.force_authenticate(self.admin)

        self.payload["variants"][0]["is_default"] = False

        response = self.client.put(
            self.detail_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_partial_update_product(self):
        self.client.force_authenticate(self.admin)

        response = self.client.patch(
            self.detail_url,
            {
                "name": "Patched Product",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.name,
            "Patched Product",
        )

    def test_update_non_existing_product(self):
        self.client.force_authenticate(self.admin)

        response = self.client.put(
            "/api/products/not-found-slug/",
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )


class ProductDeleteAPITest(BaseProductTestCase):

    def test_admin_can_delete_product(self):
        self.client.force_authenticate(self.admin)

        response = self.client.delete(
            self.detail_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

    def test_user_cannot_delete_product(self):
        self.client.force_authenticate(self.user)

        response = self.client.delete(
            self.detail_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_anonymous_cannot_delete_product(self):
        response = self.client.delete(
            self.detail_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_soft_delete_product(self):
        self.client.force_authenticate(self.admin)

        self.client.delete(
            self.detail_url,
        )

        self.product.refresh_from_db()

        self.assertFalse(
            self.product.is_active,
        )

    def test_deleted_product_not_in_list(self):
        self.client.force_authenticate(self.admin)

        self.client.delete(
            self.detail_url,
        )

        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            0,
        )

        self.assertEqual(
            len(response.data["results"]),
            0,
        )

    def test_deleted_product_returns_404(self):
        self.client.force_authenticate(self.admin)

        self.client.delete(
            self.detail_url,
        )

        response = self.client.get(
            self.detail_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_delete_non_existing_product(self):
        self.client.force_authenticate(self.admin)

        response = self.client.delete(
            "/api/products/not-found-slug/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
