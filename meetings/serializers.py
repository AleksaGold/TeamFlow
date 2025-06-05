from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from meetings.models import Meeting


class MeetingSerializer(ModelSerializer):
    """Сериализатор для модели Meeting."""

    def validate(self, data):
        """Проверяет, что время начала встречи не может быть позже времени окончания.
        Проверяет, чтобы не накладывались события."""

        # Время начала не может быть позже времени окончания

        if data["start_time"] > data["end_time"]:
            raise ValidationError(
                "Время начала встречи не может быть позже времени окончания."
            )
        # Не накладываются события

        date = data.get("date") or getattr(self.instance, "date", None)
        start_time = data.get("start_time") or getattr(
            self.instance, "start_time", None
        )
        end_time = data.get("end_time") or getattr(self.instance, "end_time", None)
        participants = data.get("participants") or getattr(
            self.instance, "participants", None
        )

        if hasattr(participants, "all"):
            participants = participants.all()

        if not all([date, start_time, end_time, participants]):
            return data

        current_meeting_id = self.instance.id if self.instance else None

        overlapping_meetings = (
            Meeting.objects.filter(participants__in=participants, date=date)
            .filter(Q(start_time__lt=end_time) & Q(end_time__gt=start_time))
            .distinct()
        )

        if current_meeting_id:
            overlapping_meetings = overlapping_meetings.exclude(id=current_meeting_id)

        if overlapping_meetings.exists():
            raise ValidationError("Указанные участники уже заняты в это время.")

        return data

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
