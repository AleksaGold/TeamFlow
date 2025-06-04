from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)

from evaluations.models import Evaluation
from evaluations.serializers import EvaluationSerializer


class EvaluationCreateAPIView(CreateAPIView):
    """Представление для создания объекта модели Evaluation."""

    serializer_class = EvaluationSerializer

    def perform_create(self, serializer):
        """Переопределение метода для автоматической привязки владельца к создаваемому объекту
        и валидация возможности проставления только одной оценки для одной задачи."""
        try:
            serializer.save(author=self.request.user)
        except IntegrityError:
            raise ValidationError("Оценка для этой задачи уже существует.")


class EvaluationListAPIView(ListAPIView):
    """Представление для просмотра списка объектов модели Evaluation."""

    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer


class EvaluationRetrieveAPIView(RetrieveAPIView):
    """Представление для просмотра одного объекта модели Evaluation."""

    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer


class EvaluationUpdateAPIView(UpdateAPIView):
    """Представление для обновления объекта модели Evaluation."""

    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer


class EvaluationDestroyAPIView(DestroyAPIView):
    """Представление для удаления объекта модели Evaluation."""

    queryset = Evaluation.objects.all()


class UserEvaluationsAPIView(ListAPIView):
    """Представление для получения списка оценок конкретного пользователя."""

    serializer_class = EvaluationSerializer

    def get_queryset(self):
        """Получает список оценок текущего пользователя."""
        return Evaluation.objects.filter(task__task_performer=self.request.user)
