from django.contrib import admin

from tasks.models import Comment, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели "Task" в административной панели."""

    list_display = (
        "pk",
        "title",
        "status",
        "deadline",
        "task_performer",
    )

    list_filter = (
        "status",
        "deadline",
        "task_performer",
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели "Comment" в административной панели."""

    list_display = (
        "pk",
        "text",
        "author",
        "task",
    )
