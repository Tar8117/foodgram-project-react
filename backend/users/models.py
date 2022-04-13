from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    first_name = models.CharField(
        'first name',
        max_length=100,
        unique=True
    )
    last_name = models.CharField(
        'last name',
        max_length=150,
    )
    email = models.EmailField(
        'email address',
        unique=True,
    )

    class Meta:
        app_label = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'Пользователь {self.first_name}'
