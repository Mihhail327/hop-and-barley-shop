import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

@pytest.mark.django_db
class TestUserAccount:
    """Тестирование системы пользователей согласно ТЗ 3.5."""

    def test_create_user_with_email(self):
        """Тест: Создание пользователя с Email вместо username."""
        user = User.objects.create_user(
            email="brewer@example.com",
            username="test_user_unique",
            password="securepassword123",
            first_name="Ivan",
            last_name="Ivanov"
        )
        assert user.email == "brewer@example.com"
        assert str(user) == "brewer@example.com"
        assert user.is_active

    def test_login_view(self, client):
        """Тест: Авторизация через форму (session-based)."""
        User.objects.create_user(email="test@test.com", password="password123", username="testuser")
        url = reverse('users:login')
        response = client.post(url, {
            'username': 'test@test.com',  # Так как USERNAME_FIELD = 'email'
            'password': 'password123'
        })
        # После входа должен быть редирект на список товаров (как в твоем settings.py)
        assert response.status_code == 302

    def test_profile_access_denied_for_anonymous(self, client):
        """Тест: Аноним не может попасть в личный кабинет."""
        url = reverse('users:profile')
        response = client.get(url)
        # Должен редиректнуть на страницу логина
        assert response.status_code == 302
        assert reverse('users:login') in response.url

    def test_profile_edit_logic(self, admin_client, client):
        """Тест: Залогиненный пользователь может менять свои данные."""
        url = reverse('users:profile')
        response = admin_client.post(url, {
            'first_name': 'NewName',
            'last_name': 'NewLastName',
            'email': 'admin@example.com'
        })
        assert response.status_code == 302  # Проверяем редирект после сохранения
        # Проверяем, что данные в базе обновились
        user = User.objects.get(email='admin@example.com')
        assert user.first_name == 'NewName'
