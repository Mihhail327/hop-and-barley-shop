import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def admin_user(db):
    try:
        user = User.objects.get(email="admin@example.com")
    except User.DoesNotExist:
        user = User.objects.create_superuser(
            email="admin@example.com",
            password="password",
            username="admin",
            first_name="Admin",
            last_name="User"
        )
    return user
