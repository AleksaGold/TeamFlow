from rest_framework.serializers import (ModelSerializer, StringRelatedField,
                                        ValidationError)

from evaluations.models import Evaluation


class EvaluationSerializer(ModelSerializer):
    """Сериализатор для модели Evaluation."""

    task_performer = StringRelatedField(source="task.task_performer", read_only=True)

    class Meta:
        model = Evaluation
        fields = (
            "id",
            "task",
            "author",
            "score",
            "comment",
            "created_at",
            "task_performer",
        )
        read_only_fields = ("task_performer",)
