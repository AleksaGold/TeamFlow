from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)

from teams.models import Team
from teams.serializers import TeamDetailSerializer, TeamSerializer


class TeamCreateAPIView(CreateAPIView):
    """Представление для создания объекта модели Team."""

    serializer_class = TeamSerializer


class TeamListAPIView(ListAPIView):
    """Представление для просмотра списка объектов модели Team."""

    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamRetrieveAPIView(RetrieveAPIView):
    """Представление для просмотра одного объекта модели Team."""

    queryset = Team.objects.all()
    serializer_class = TeamDetailSerializer


class TeamUpdateAPIView(UpdateAPIView):
    """Представление для обновления объекта модели Team."""

    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamDestroyAPIView(DestroyAPIView):
    """Представление для удаления объекта модели Team."""

    queryset = Team.objects.all()
