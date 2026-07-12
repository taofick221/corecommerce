from rest_framework import status
from django.urls import reverse
from .base import BaseCartTestCase

from apps.products.tests.factories import ProductVariantFactory


class CartDetailAPITest(BaseCartTestCase):

    def test_get_cart_success(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(self.cart_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_get_cart_requires_authentication(self):
        response = self.client.get(self.cart_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_get_empty_cart(self):
        self.cart.items.all().delete()

        self.client.force_authenticate(self.user)

        response = self.client.get(self.cart_url)

        self.assertEqual(
            len(response.data["items"]),
            0,
        )

    def test_cart_returns_items(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(self.cart_url)

        self.assertEqual(
            len(response.data["items"]),
            1,
        )

    def test_cart_returns_subtotal(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(self.cart_url)

        self.assertEqual(
            response.data["subtotal"],
            self.cart.subtotal,
        )


    def test_cart_returns_total(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(self.cart_url)

        self.assertEqual(
            response.data["total"],
            self.cart.total,
        )


class AddToCartAPITest(BaseCartTestCase):

    def test_add_to_cart_success(self):
        self.client.force_authenticate(self.user)

        variant = ProductVariantFactory()

        response = self.client.post(
            self.add_to_cart_url,
            {
                "variant_id": variant.id,
                "quantity": 2,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_add_existing_item_increases_quantity(self):
        self.client.force_authenticate(self.user)

        initial_quantity = self.cart_item.quantity

        response = self.client.post(
            self.add_to_cart_url,
            {
                "variant_id": self.variant.id,
                "quantity": 2,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.cart_item.refresh_from_db()

        self.assertEqual(
            self.cart_item.quantity,
            initial_quantity + 2,
        )

    def test_add_invalid_variant(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(
            self.add_to_cart_url,
            {
                "variant_id": 99999,
                "quantity": 1,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_add_inactive_product(self):
        self.client.force_authenticate(self.user)

        self.product.is_active = False
        self.product.save()

        response = self.client.post(
            self.add_to_cart_url,
            {
                "variant_id": self.variant.id,
                "quantity": 1,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_add_soft_deleted_product(self):
        from django.utils import timezone

        self.client.force_authenticate(self.user)

        self.product.deleted_at = timezone.now()
        self.product.save()

        response = self.client.post(
            self.add_to_cart_url,
            {
                "variant_id": self.variant.id,
                "quantity": 1,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_add_not_enough_stock(self):
        self.client.force_authenticate(self.user)

        self.variant.stock = 2
        self.variant.save()

        response = self.client.post(
            self.add_to_cart_url,
            {
                "variant_id": self.variant.id,
                "quantity": 10,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_add_invalid_quantity(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(
            self.add_to_cart_url,
            {
                "variant_id": self.variant.id,
                "quantity": 0,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_add_requires_authentication(self):
        response = self.client.post(
            self.add_to_cart_url,
            {
                "variant_id": self.variant.id,
                "quantity": 1,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
    from django.urls import reverse


class UpdateCartItemAPITest(BaseCartTestCase):

    def test_update_cart_item_success(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(
            self.update_cart_item_url,
            {
                "quantity": 5,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.cart_item.refresh_from_db()

        self.assertEqual(
            self.cart_item.quantity,
            5,
        )

    def test_update_cart_item_to_zero_deletes_item(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(
            self.update_cart_item_url,
            {
                "quantity": 0,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertFalse(
            self.cart.items.filter(
                id=self.cart_item.id,
            ).exists()
        )

    def test_update_cart_item_not_enough_stock(self):
        self.client.force_authenticate(self.user)

        self.variant.stock = 2
        self.variant.save()

        response = self.client.patch(
            self.update_cart_item_url,
            {
                "quantity": 10,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_update_cart_item_negative_quantity(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(
            self.update_cart_item_url,
            {
                "quantity": -1,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_update_cart_item_not_found(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(
            reverse(
                "update_cart_item",
                kwargs={
                    "item_id": 99999,
                },
            ),
            {
                "quantity": 2,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_update_cart_item_requires_authentication(self):
        response = self.client.patch(
            self.update_cart_item_url,
            {
                "quantity": 2,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


class RemoveCartItemAPITest(BaseCartTestCase):

    def test_remove_cart_item_success(self):
        self.client.force_authenticate(self.user)

        response = self.client.delete(
            self.remove_cart_item_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertFalse(
            self.cart.items.filter(
                id=self.cart_item.id,
            ).exists()
        )

    def test_remove_cart_item_not_found(self):
        self.client.force_authenticate(self.user)

        response = self.client.delete(
            reverse(
                "remove_cart_item",
                kwargs={
                    "item_id": 99999,
                },
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_remove_cart_item_requires_authentication(self):
        response = self.client.delete(
            self.remove_cart_item_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


class ClearCartAPITest(BaseCartTestCase):

    def test_clear_cart_success(self):
        self.client.force_authenticate(self.user)

        response = self.client.delete(
            self.clear_cart_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.cart.refresh_from_db()

        self.assertEqual(
            self.cart.items.count(),
            0,
        )

    def test_clear_empty_cart(self):
        self.client.force_authenticate(self.user)

        self.cart.items.all().delete()

        response = self.client.delete(
            self.clear_cart_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.cart.refresh_from_db()

        self.assertEqual(
            self.cart.items.count(),
            0,
        )

    def test_clear_cart_requires_authentication(self):
        response = self.client.delete(
            self.clear_cart_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )