from django.contrib import admin

from evaluations.models import Evaluation


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели "Evaluation" в административной панели."""

    list_display = (
        "pk",
        "task",
        "author",
        "score",
    )
