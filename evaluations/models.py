from django.db import models

from config import settings

NULLABLE = {"blank": True, "null": True}


class Evaluation(models.Model):
    """Модель Evaluation для хранения информации об оценках."""

    SCORE_CHOICES = [(i, str(i)) for i in range(1, 6)]

    task = models.ForeignKey(
        "tasks.Task",
        on_delete=models.CASCADE,
        verbose_name="Задача, к которой относится оценка",
        related_name="evaluations",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Автор оценки",
        related_name="evaluations",
        **NULLABLE,
    )
    score = models.PositiveIntegerField(choices=SCORE_CHOICES, verbose_name="Оценка")
    comment = models.TextField(verbose_name="Комментарий к оценке", **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    @property
    def evaluated_user(self):
        return self.task.task_performer

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"

    def __str__(self):
        """Возвращает строковое представление объекта."""
        return f"Оценка от {self.author} - {self.score} за задачу {self.task}"
