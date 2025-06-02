from django.db import models

from config import settings

NULLABLE = {"blank": True, "null": True}


class Task(models.Model):
    """Модель Task для хранения информации о задачах."""

    STATUSES = [
        ("open", "open"),
        ("in_progress", "in_progress"),
        ("completed", "completed"),
    ]

    title = models.CharField(max_length=100, verbose_name="Название задачи")
    description = models.TextField(verbose_name="Описание задачи")
    status = models.CharField(
        max_length=20, choices=STATUSES, verbose_name="Статус задачи", default="open"
    )
    deadline = models.DateField(verbose_name="Дедлайн")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь, который создал задачу",
        related_name="created_tasks",
        **NULLABLE,
    )
    task_performer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Исполнитель которому назначена задача",
        related_name="performer_tasks",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        """Возвращает строковое представление объекта."""
        return self.title


class Comment(models.Model):
    """Модель Comment для хранения комментариев к задачам."""

    text = models.TextField(verbose_name="Текст комментария")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Автор комментария",
        related_name="comments",
        **NULLABLE,
    )
    task = models.ForeignKey(
        "tasks.Task",
        on_delete=models.CASCADE,
        verbose_name="Задача, к которой относится комментарий",
        related_name="comments",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-created_at"]

    def __str__(self):
        """Возвращает строковое представление объекта."""
        return f"Комментарий от {self.author} - {self.created_at}"
