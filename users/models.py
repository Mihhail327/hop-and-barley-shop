from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Уникальный email — теперь это наш логин
    email = models.EmailField(unique=True, verbose_name='Email Address')

    # Делаем имена обязательными на уровне БД
    first_name = models.CharField(max_length=150, verbose_name='First Name')
    last_name = models.CharField(max_length=150, verbose_name='Last Name')

    # Указываем, что email — основной идентификатор
    USERNAME_FIELD = 'email'

    # Убираем email из REQUIRED_FIELDS (так как он уже USERNAME_FIELD)
    # Но оставляем username и имена для корректной работы админки и форм
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email