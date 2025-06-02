from rest_framework.serializers import ModelSerializer

from tasks.models import Comment, Task


class TaskSerializer(ModelSerializer):
    """Сериализатор для модели Task."""

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "status",
            "deadline",
            "author",
            "task_performer",
        )


class CommentSerializer(ModelSerializer):
    """Сериализатор для модели Comment."""

    class Meta:
        model = Comment
        fields = (
            "id",
            "text",
            "author",
            "task",
            "created_at",
        )


class TaskDetailSerializer(ModelSerializer):
    """Сериализатор для одного объекта Task."""

    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "status",
            "deadline",
            "author",
            "task_performer",
            "comments",
        )
