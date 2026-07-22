from django.test import TestCase

from apps.users.serializers import UserSerializer

from .factories import UserFactory


class UserSerializerTest(TestCase):

    def test_valid_serializer(self):

        serializer = UserSerializer(
            data={
                "email": "test@test.com",
                "password": "Test123@",
                "confirm_password": "Test123@",
            }
        )

        self.assertTrue(serializer.is_valid())

    def test_password_mismatch(self):

        serializer = UserSerializer(
            data={
                "email": "test@test.com",
                "password": "Test123@",
                "confirm_password": "Wrong123@",
            }
        )

        self.assertFalse(serializer.is_valid())

    def test_duplicate_email(self):

        UserFactory(email="test@test.com")

        serializer = UserSerializer(
            data={
                "email": "test@test.com",
                "password": "Test123@",
                "confirm_password": "Test123@",
            }
        )

        self.assertFalse(serializer.is_valid())

    def test_missing_password(self):

        serializer = UserSerializer(
            data={
                "email": "test@test.com",
                "confirm_password": "Test123@",
            }
        )

        self.assertFalse(serializer.is_valid())

    def test_missing_confirm_password(self):

        serializer = UserSerializer(
            data={
                "email": "test@test.com",
                "password": "Test123@",
            }
        )

        self.assertFalse(serializer.is_valid())

    def test_create_user(self):

        serializer = UserSerializer(
            data={
                "email": "test@test.com",
                "password": "Test123@",
                "confirm_password": "Test123@",
            }
        )

        self.assertTrue(serializer.is_valid())

        user = serializer.save()

        self.assertEqual(
            user.email,
            "test@test.com",
        )

    def test_password_is_hashed(self):

        serializer = UserSerializer(
            data={
                "email": "test@test.com",
                "password": "Test123@",
                "confirm_password": "Test123@",
            }
        )

        serializer.is_valid()

        user = serializer.save()

        self.assertTrue(user.check_password("Test123@"))
