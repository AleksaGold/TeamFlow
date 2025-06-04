from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    """Сериализатор для модели User."""

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "role",
            "is_superuser",
            "is_active",
            "password",
        )


class MemberSerializer(ModelSerializer):
    """Сериализатор для использования модели User для вывода участников команды."""

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "role",
            "is_active",
        )
