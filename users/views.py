from django.db.models import Avg
from django.utils.dateparse import parse_date
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.response import Response

from evaluations.models import Evaluation
from users.models import User
from users.serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    """Представление для создания нового объекта модели User."""

    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """Сохраняет сериализованные данные при регистрации пользователя и хэширует пароль."""
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    """Представление для создания нового объекта модели User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateAPIView(UpdateAPIView):
    """Представление для обновления объекта модели User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDeleteAPIView(DestroyAPIView):
    """Представление для удаления объекта модели User."""

    queryset = User.objects.all()


class UserAverageScoreView(RetrieveAPIView):
    """Представление для получения средней оценки пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        start = parse_date(request.query_params.get("start"))
        end = parse_date(request.query_params.get("end"))

        evaluations = Evaluation.objects.filter(task__task_performer=user)

        if start:
            evaluations = evaluations.filter(created_at__gte=start)
        if end:
            evaluations = evaluations.filter(created_at__lte=end)

        avg_score = evaluations.aggregate(avg=Avg("score"))["avg"]

        return Response(
            {
                "user_id": user.id,
                "task_performer": user.email,
                "average_score": round(avg_score, 2) if avg_score else None,
                "period": {"start": start, "end": end},
            }
        )
