from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from apps.products.permissions import IsAdminOrReadOnly

User = get_user_model()


class ProductPermissionTest(TestCase):

    def setUp(self):
        self.permission = IsAdminOrReadOnly()
        self.factory = APIRequestFactory()

        self.admin = User.objects.create_user(
            email="admin@example.com",
            password="password123",
            is_staff=True,
        )

        self.user = User.objects.create_user(
            email="user@example.com",
            password="password123",
        )

    def test_anyone_can_read(self):
        request = self.factory.get(
            "/api/products/",
        )

        request.user = self.user

        self.assertTrue(
            self.permission.has_permission(
                request,
                None,
            )
        )

    def test_admin_can_write(self):
        request = self.factory.post(
            "/api/products/",
        )

        request.user = self.admin

        self.assertTrue(
            self.permission.has_permission(
                request,
                None,
            )
        )

    def test_normal_user_cannot_write(self):
        request = self.factory.post(
            "/api/products/",
        )

        request.user = self.user

        self.assertFalse(
            self.permission.has_permission(
                request,
                None,
            )
        )

    def test_anonymous_can_read(self):
        request = self.factory.get(
            "/api/products/",
        )

        request.user = None

        self.assertTrue(
            self.permission.has_permission(
                request,
                None,
            )
        )

    def test_anonymous_cannot_write(self):
        request = self.factory.post(
            "/api/products/",
        )

        request.user = None

        self.assertFalse(
            self.permission.has_permission(
                request,
                None,
            )
        )
