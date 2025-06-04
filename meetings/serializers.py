from rest_framework.serializers import ModelSerializer

from meetings.models import Meeting


class MeetingSerializer(ModelSerializer):
    """Сериализатор для модели Meeting."""

    class Meta:
        model = Meeting
        fields = (
            "id",
            "title",
            "description",
            "date",
            "start_time",
            "end_time",
            "organizer",
            "participants",
        )
