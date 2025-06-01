
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("user/", include("users.urls", namespace="user")),
    path("evaluation/", include("evaluations.urls", namespace="evaluation")),
    path("meeting/", include("meetings.urls", namespace="meeting")),
    path("task/", include("tasks.urls", namespace="task")),
    path("team/", include("teams.urls", namespace="team")),
]
