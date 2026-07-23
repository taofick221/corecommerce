from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.products.services import (create_product, soft_delete_product,
                                    update_product)

from .factories import (BrandFactory, CategoryFactory, ProductFactory,
                        ProductImageFactory, ProductVariantFactory)


class CreateProductServiceTest(TestCase):

    def setUp(self):
        self.category = CategoryFactory()
        self.brand = BrandFactory()

    def get_payload(self):
        return {
            "name": "Nike Air Max",
            "description": "Running Shoe",
            "category": self.category,
            "brand": self.brand,
            "is_active": True,
            "variants": [
                {
                    "size": "42",
                    "color": "Black",
                    "price": 120,
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

    def test_create_product_success(self):
        product = create_product(self.get_payload())

        self.assertEqual(
            product.name,
            "Nike Air Max",
        )

        self.assertEqual(
            product.variants.count(),
            1,
        )

        self.assertEqual(
            product.images.count(),
            1,
        )

    def test_create_without_variant(self):
        payload = self.get_payload()

        payload["variants"] = []

        with self.assertRaises(
            ValidationError,
        ):
            create_product(payload)

    def test_duplicate_sku(self):
        payload = self.get_payload()

        payload["variants"] = [
            {
                "size": "42",
                "color": "Black",
                "price": 100,
                "stock": 5,
                "sku": "SKU100",
                "is_default": True,
            },
            {
                "size": "43",
                "color": "White",
                "price": 120,
                "stock": 10,
                "sku": "SKU100",
                "is_default": False,
            },
        ]

        with self.assertRaises(
            ValidationError,
        ):
            create_product(payload)

    def test_duplicate_variant(self):
        payload = self.get_payload()

        payload["variants"] = [
            {
                "size": "42",
                "color": "Black",
                "price": 100,
                "stock": 5,
                "sku": "SKU100",
                "is_default": True,
            },
            {
                "size": "42",
                "color": "Black",
                "price": 120,
                "stock": 10,
                "sku": "SKU200",
                "is_default": False,
            },
        ]

        with self.assertRaises(
            ValidationError,
        ):
            create_product(payload)

    def test_multiple_default_variant(self):
        payload = self.get_payload()

        payload["variants"] = [
            {
                "size": "42",
                "color": "Black",
                "price": 100,
                "stock": 5,
                "sku": "SKU100",
                "is_default": True,
            },
            {
                "size": "43",
                "color": "White",
                "price": 120,
                "stock": 10,
                "sku": "SKU200",
                "is_default": True,
            },
        ]

        with self.assertRaises(
            ValidationError,
        ):
            create_product(payload)

    def test_multiple_primary_image(self):
        payload = self.get_payload()

        payload["images"] = [
            {
                "alt_text": "Front",
                "order": 0,
                "is_primary": True,
            },
            {
                "alt_text": "Back",
                "order": 1,
                "is_primary": True,
            },
        ]

        with self.assertRaises(
            ValidationError,
        ):
            create_product(payload)

    def test_create_without_image(self):
        payload = self.get_payload()

        payload["images"] = []

        product = create_product(payload)

        self.assertEqual(
            product.images.count(),
            0,
        )

    def test_product_name_saved(self):
        payload = self.get_payload()

        payload["name"] = "Jordan 1"

        product = create_product(payload)

        self.assertEqual(
            product.name,
            "Jordan 1",
        )

    def test_product_slug_created(self):
        product = create_product(self.get_payload())

        self.assertTrue(
            product.slug,
        )

    def test_variant_saved(self):
        product = create_product(self.get_payload())

        variant = product.variants.first()

        self.assertEqual(
            variant.size,
            "42",
        )

        self.assertEqual(
            variant.color,
            "black",
        )

        self.assertEqual(
            variant.stock,
            10,
        )

    def test_primary_image_saved(self):
        product = create_product(self.get_payload())

        image = product.images.first()

        self.assertTrue(
            image.is_primary,
        )

    def test_create_returns_product_instance(self):
        product = create_product(self.get_payload())

        self.assertIsNotNone(
            product.id,
        )

        self.assertEqual(
            product.__class__.__name__,
            "Product",
        )


class UpdateProductServiceTest(TestCase):

    def setUp(self):
        self.product = ProductFactory()

        self.variant = ProductVariantFactory(
            product=self.product,
            is_default=True,
        )

        self.image = ProductImageFactory(
            product=self.product,
            is_primary=True,
        )

    def get_payload(self):
        return {
            "name": "Updated Product",
            "description": "Updated Description",
            "category": self.product.category,
            "brand": self.product.brand,
            "is_active": True,
            "variants": [
                {
                    "id": self.variant.id,
                    "size": "43",
                    "color": "White",
                    "price": 200,
                    "stock": 20,
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

    def test_update_product_success(self):
        product = update_product(
            self.product,
            self.get_payload(),
        )

        self.assertEqual(
            product.name,
            "Updated Product",
        )

    def test_update_description(self):
        update_product(
            self.product,
            self.get_payload(),
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.description,
            "Updated Description",
        )

    def test_update_variant(self):
        update_product(
            self.product,
            self.get_payload(),
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
            20,
        )

    def test_update_image(self):
        update_product(
            self.product,
            self.get_payload(),
        )

        self.image.refresh_from_db()

        self.assertEqual(
            self.image.alt_text,
            "Updated Image",
        )

    def test_update_returns_product(self):
        product = update_product(
            self.product,
            self.get_payload(),
        )

        self.assertEqual(
            product.id,
            self.product.id,
        )

    def test_update_without_variant(self):
        payload = self.get_payload()

        payload["variants"] = []

        with self.assertRaises(
            ValidationError,
        ):
            update_product(
                self.product,
                payload,
            )

    def test_add_new_variant(self):
        payload = self.get_payload()

        payload["variants"].append(
            {
                "size": "44",
                "color": "Black",
                "price": 250,
                "stock": 5,
                "sku": "SKU200",
                "is_default": False,
            }
        )

        update_product(
            self.product,
            payload,
        )

        self.assertEqual(
            self.product.variants.count(),
            2,
        )

    def test_remove_variant(self):
        second_variant = ProductVariantFactory(
            product=self.product,
            sku="SKU300",
        )

        payload = self.get_payload()

        update_product(
            self.product,
            payload,
        )

        self.assertFalse(
            self.product.variants.filter(
                id=second_variant.id,
            ).exists()
        )

    def test_add_new_image(self):
        payload = self.get_payload()

        payload["images"].append(
            {
                "alt_text": "Side Image",
                "order": 1,
                "is_primary": False,
            }
        )

        update_product(
            self.product,
            payload,
        )

        self.assertEqual(
            self.product.images.count(),
            2,
        )

    def test_remove_image(self):
        second_image = ProductImageFactory(
            product=self.product,
        )

        payload = self.get_payload()

        update_product(
            self.product,
            payload,
        )

        self.assertFalse(
            self.product.images.filter(
                id=second_image.id,
            ).exists()
        )

    def test_duplicate_sku(self):
        payload = self.get_payload()

        payload["variants"].append(
            {
                "size": "44",
                "color": "Black",
                "price": 250,
                "stock": 5,
                "sku": self.variant.sku,
                "is_default": False,
            }
        )

        with self.assertRaises(
            ValidationError,
        ):
            update_product(
                self.product,
                payload,
            )

    def test_duplicate_variant(self):
        payload = self.get_payload()

        payload["variants"].append(
            {
                "size": "43",
                "color": "White",
                "price": 250,
                "stock": 5,
                "sku": "SKU999",
                "is_default": False,
            }
        )

        with self.assertRaises(
            ValidationError,
        ):
            update_product(
                self.product,
                payload,
            )

    def test_without_default_variant(self):
        payload = self.get_payload()

        payload["variants"][0]["is_default"] = False

        with self.assertRaises(
            ValidationError,
        ):
            update_product(
                self.product,
                payload,
            )

    def test_variant_not_found(self):
        payload = self.get_payload()

        payload["variants"][0]["id"] = 99999

        with self.assertRaises(
            ValidationError,
        ):
            update_product(
                self.product,
                payload,
            )

    def test_image_not_found(self):
        payload = self.get_payload()

        payload["images"][0]["id"] = 99999

        with self.assertRaises(
            ValidationError,
        ):
            update_product(
                self.product,
                payload,
            )


class SoftDeleteProductServiceTest(TestCase):

    def setUp(self):
        self.product = ProductFactory()

    def test_soft_delete_product(self):
        soft_delete_product(
            self.product,
        )

        self.product.refresh_from_db()

        self.assertFalse(
            self.product.is_active,
        )

    def test_sets_deleted_at(self):
        soft_delete_product(
            self.product,
        )

        self.product.refresh_from_db()

        self.assertIsNotNone(
            self.product.deleted_at,
        )

    def test_product_still_exists_in_database(self):
        soft_delete_product(
            self.product,
        )

        self.assertTrue(
            self.product.__class__.all_objects.filter(
                id=self.product.id,
            ).exists()
        )

    def test_product_removed_from_default_manager(self):
        soft_delete_product(
            self.product,
        )

        self.assertFalse(
            self.product.__class__.objects.filter(
                id=self.product.id,
            ).exists()
        )

    def test_deleted_at_is_recent(self):
        before = timezone.now()

        soft_delete_product(
            self.product,
        )

        self.product.refresh_from_db()

        self.assertGreaterEqual(
            self.product.deleted_at,
            before,
        )
