from datetime import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from tasks.models import Comment, Task
from users.models import User


class TaskTestCase(APITestCase):
    """Тесты для модели Task."""

    def setUp(self):
        """Окружение для тестов."""
        self.client_1 = APIClient()
        self.client_2 = APIClient()

        self.user_role = User.objects.create(email="user@test.test", role="user")
        self.manager_role = User.objects.create(
            email="manager@test.test", role="manager"
        )

        self.client_1.force_authenticate(user=self.user_role)
        self.client_2.force_authenticate(user=self.manager_role)

        self.task_1 = Task.objects.create(
            title="Test task",
            description="Test description",
            status="open",
            deadline="2025-06-06",
            author=self.manager_role,
            task_performer=self.user_role,
        )
        self.task_2 = Task.objects.create(
            title="Some task",
            description="Some description",
            status="in-progress",
            deadline="2025-08-06",
            author=self.manager_role,
            task_performer=self.manager_role,
        )

    def test_task_create(self):
        """Тестирование создания новой задачи."""
        url = reverse("task:create_task")
        data = {
            "title": "New task",
            "description": "New task description",
            "status": "open",
            "deadline": "2025-07-06",
            "task_performer": self.user_role.pk,
        }

        response = self.client_1.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Task.objects.count(), 2)

        response = self.client_2.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)

    def test_task_retrieve(self):
        """Тестирование просмотра одной задачи."""
        url = reverse("task:retrieve_task", args=(self.task_1.pk,))
        response = self.client_1.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.task_1.title)
        self.assertEqual(data.get("comments"), [])

    def test_task_update(self):
        """Тестирование обновления задачи."""
        url = reverse("task:update_task", args=(self.task_1.pk,))
        data = {"status": "completed"}

        response = self.client_1.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.task_1.status, "open")

        response = self.client_2.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("status"), "completed")

    def test_task_delete(self):
        """Тестирование удаления задачи."""
        url = reverse("task:destroy_task", args=(self.task_1.pk,))

        response = self.client_1.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Task.objects.count(), 2)

        response = self.client_2.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 1)

    def test_task_list(self):
        """Тестирование просмотра списка задач."""
        url = reverse("task:tasks_list")
        response = self.client_2.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 2)


class CommentTestCase(APITestCase):
    """Тесты для модели Comment."""

    def setUp(self):
        """Окружение для тестов."""
        self.user_role = User.objects.create(email="user@test.test", role="user")
        self.manager_role = User.objects.create(
            email="manager@test.test", role="manager"
        )

        self.client.force_authenticate(user=self.user_role)

        self.task = Task.objects.create(
            title="Test task",
            description="Test description",
            status="open",
            deadline="2025-06-06",
            author=self.manager_role,
            task_performer=self.user_role,
        )
        self.comment = Comment.objects.create(
            text="Test comment", task=self.task, created_at=datetime.now()
        )

    def test_comment_create(self):
        """Тестирование создания нового комментария."""
        url = reverse("task:create_comment")
        data = {
            "text": "New comment",
            "task": self.task.pk,
            "created_at": datetime.now(),
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)

    def test_comment_retrieve(self):
        """Тестирование просмотра одного комментария."""
        url = reverse("task:retrieve_comment", args=(self.comment.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("text"), self.comment.text)
        self.assertEqual(data.get("task"), self.task.pk)

    def test_comment_update(self):
        """Тестирование обновления комментария"""
        url = reverse("task:update_comment", args=(self.comment.pk,))
        data = {"text": "add something"}

        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("text"), "add something")

    def test_comment_delete(self):
        """Тестирование удаления комментария."""
        url = reverse("task:destroy_comment", args=(self.comment.pk,))

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

    def test_comment_list(self):
        """Тестирование просмотра списка комментариев."""
        url = reverse("task:comments_list")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
