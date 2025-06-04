from django.db import models

from config import settings

NULLABLE = {"blank": True, "null": True}


class Team(models.Model):
    """Модель Team для хранения информации о командах."""

    name = models.CharField(max_length=100, verbose_name="Название команды")
    description = models.TextField(verbose_name="Описание команды", **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    team_admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Администратор команды",
        **NULLABLE,
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name="Участники команды", related_name="teams"
    )

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"

    def __str__(self):
        """Возвращает строковое представление объекта."""
        return f"Команда - {self.name} Админ команды - {self.team_admin}"
