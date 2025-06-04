from rest_framework.serializers import ModelSerializer

from teams.models import Team
from users.serializers import MemberSerializer


class TeamSerializer(ModelSerializer):
    """Сериализатор для модели Team."""

    class Meta:
        model = Team
        fields = (
            "id",
            "name",
            "description",
            "created_at",
            "team_admin",
            "members",
        )


class TeamDetailSerializer(ModelSerializer):
    """Сериализатор для одного объекта Team."""

    team_admin = MemberSerializer(read_only=True)
    members = MemberSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = (
            "id",
            "name",
            "description",
            "created_at",
            "team_admin",
            "members",
        )
