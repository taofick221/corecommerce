from django.urls import reverse
from rest_framework.test import APITestCase

from .factories import UserFactory


class BaseUserTestCase(APITestCase):

    def setUp(self):

        self.user = UserFactory()

        self.register_url = reverse(
            "register",
        )

        self.login_url = reverse(
            "login",
        )

        self.refresh_url = reverse(
            "token_refresh",
        )
