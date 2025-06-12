from django.contrib import admin

from meetings.models import Meeting


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели "Meeting" в административной панели."""

    list_display = (
        "pk",
        "title",
        "date",
        "organizer",
    )

    list_filter = (
        "date",
        "organizer",
    )
