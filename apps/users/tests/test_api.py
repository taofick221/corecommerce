from unittest.mock import patch

from rest_framework import status

from .base import BaseUserTestCase


class RegisterAPITest(BaseUserTestCase):

    @patch(
        "apps.users.views.RegisterRateThrottle.allow_request",
        return_value=True,
    )
    def test_register_success(self, mock_allow_request):

        response = self.client.post(
            self.register_url,
            {
                "email": "new@test.com",
                "password": "Test123@",
                "confirm_password": "Test123@",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    @patch(
        "apps.users.views.RegisterRateThrottle.allow_request",
        return_value=True,
    )
    def test_duplicate_email(self, mock_allow_request):

        response = self.client.post(
            self.register_url,
            {
                "email": self.user.email,
                "password": "Test123@",
                "confirm_password": "Test123@",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    @patch(
        "apps.users.views.RegisterRateThrottle.allow_request",
        return_value=True,
    )
    def test_password_mismatch(self, mock_allow_request):

        response = self.client.post(
            self.register_url,
            {
                "email": "new@test.com",
                "password": "Test123@",
                "confirm_password": "Wrong123@",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    @patch(
        "apps.users.views.RegisterRateThrottle.allow_request",
        return_value=True,
    )
    def test_weak_password(self, mock_allow_request):

        response = self.client.post(
            self.register_url,
            {
                "email": "new@test.com",
                "password": "123",
                "confirm_password": "123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    @patch(
        "apps.users.views.RegisterRateThrottle.allow_request",
        return_value=True,
    )
    def test_missing_fields(self, mock_allow_request):

        response = self.client.post(
            self.register_url,
            {
                "email": "new@test.com",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


class LoginAPITest(BaseUserTestCase):

    def test_login_success(self):

        response = self.client.post(
            self.login_url,
            {
                "email": self.user.email,
                "password": "Test123@",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn(
            "access",
            response.data,
        )

        self.assertIn(
            "refresh",
            response.data,
        )

    def test_wrong_password(self):

        response = self.client.post(
            self.login_url,
            {
                "email": self.user.email,
                "password": "Wrong123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_unknown_email(self):

        response = self.client.post(
            self.login_url,
            {
                "email": "unknown@test.com",
                "password": "Test123@",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_refresh_token(self):

        login = self.client.post(
            self.login_url,
            {
                "email": self.user.email,
                "password": "Test123@",
            },
            format="json",
        )

        response = self.client.post(
            self.refresh_url,
            {
                "refresh": login.data["refresh"],
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn(
            "access",
            response.data,
        )

    def test_invalid_refresh_token(self):

        response = self.client.post(
            self.refresh_url,
            {
                "refresh": "invalid-token",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )