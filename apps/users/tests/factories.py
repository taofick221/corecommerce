import factory

from apps.users.models import User


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    email = factory.Sequence(
        lambda n: f"user{n}@test.com"
    )

    password = factory.PostGenerationMethodCall(
        "set_password",
        "Test123@",
    )


class AdminFactory(UserFactory):

    is_staff = True
    is_superuser = True