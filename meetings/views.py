from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)

from meetings.models import Meeting
from meetings.serializers import MeetingSerializer


class MeetingCreateAPIView(CreateAPIView):
    """Представление для создания объекта модели Meeting."""

    serializer_class = MeetingSerializer

    def perform_create(self, serializer):
        """Переопределение метода для автоматической привязки организатора ко встрече."""
        serializer.save(organizer=self.request.user)


class MeetingListAPIView(ListAPIView):
    """Представление для просмотра списка объектов модели Meeting."""

    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer


class MeetingRetrieveAPIView(RetrieveAPIView):
    """Представление для просмотра одного объекта модели Meeting."""

    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer


class MeetingUpdateAPIView(UpdateAPIView):
    """Представление для обновления объекта модели Meeting."""

    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer


class MeetingDestroyAPIView(DestroyAPIView):
    """Представление для удаления объекта модели Meeting."""

    queryset = Meeting.objects.all()


class UserMeetingsAPIView(ListAPIView):
    """Представление для получения списка всех встреч пользователя."""

    serializer_class = MeetingSerializer

    def get_queryset(self):
        """Получает список встреч текущего пользователя."""
        return Meeting.objects.filter(participants=self.request.user)
