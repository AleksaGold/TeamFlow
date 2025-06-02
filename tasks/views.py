from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)

from tasks.models import Comment, Task
from tasks.serializers import (CommentSerializer, TaskDetailSerializer,
                               TaskSerializer)


class TaskCreateAPIView(CreateAPIView):
    """Представление для создания объекта модели Task."""

    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        """Переопределение метода для автоматической привязки автора к создаваемой задаче."""
        serializer.save(author=self.request.user)


class TaskListAPIView(ListAPIView):
    """Представление для просмотра списка объектов модели Task."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskRetrieveAPIView(RetrieveAPIView):
    """Представление для просмотра одного объекта модели Task."""

    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer


class TaskUpdateAPIView(UpdateAPIView):
    """Представление для обновления объекта модели Task."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDestroyAPIView(DestroyAPIView):
    """Представление для удаления объекта модели Task."""

    queryset = Task.objects.all()


class CommentCreateAPIView(CreateAPIView):
    """Представление для создания объекта модели Comment."""

    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        """Переопределение метода для автоматической привязки владельца к создаваемому объекту."""
        serializer.save(author=self.request.user)


class CommentListAPIView(ListAPIView):
    """Представление для просмотра списка объектов модели Comment."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentRetrieveAPIView(RetrieveAPIView):
    """Представление для просмотра одного объекта модели Comment."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentUpdateAPIView(UpdateAPIView):
    """Представление для обновления объекта модели Comment."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentDestroyAPIView(DestroyAPIView):
    """Представление для удаления объекта модели Comment."""

    queryset = Comment.objects.all()
