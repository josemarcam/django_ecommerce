import pytest

from users.models import User

pytestmark = pytest.mark.django_db

def test_create_user():
    user = User.objects.create_user(
        username="teste",email="email@test.com",password="123qwe"
    )

    assert user.username == "teste"
    assert user.email == "email@test.com"
    assert user.is_active
    assert not user.is_staff