from django.contrib import admin

from teams.models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели "Team" в административной панели."""

    list_display = (
        "pk",
        "name",
        "team_admin",
    )
