from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """Модель User для хранения информации о пользователях веб-приложения."""

    ROLES = [
        ("user", "user"),
        ("manager", "manager"),
        ("admin", "admin"),
    ]

    username = None
    email = models.EmailField(
        unique=True, verbose_name="Электронная почта пользователя (email)"
    )

    first_name = models.CharField(
        max_length=50, verbose_name="Имя пользователя", **NULLABLE
    )
    last_name = models.CharField(
        max_length=50, verbose_name="Фамилия пользователя", **NULLABLE
    )
    role = models.CharField(
        max_length=20,
        choices=ROLES,
        verbose_name="Роль пользователя",
        default="user",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        """Возвращает строковое представление объекта."""
        return f"{self.email} - {self.role}"
