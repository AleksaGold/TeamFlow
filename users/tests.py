from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):
    """Тесты для модели User."""

    def setUp(self):
        """Окружение для тестов."""
        self.user_role = User.objects.create(email="user@test.test", role="user")
        self.manager_role = User.objects.create(
            email="manager@test.test", role="manager"
        )

        self.client.force_authenticate(user=self.user_role)

    def test_user_create(self):
        """Тестирование создания нового пользователя."""
        url = reverse("user:register")
        data = {
            "email": "admin@test.test",
            "role": "admin",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_user_update(self):
        """Тестирование обновления профиля пользователя."""
        url = reverse("user:update_user", args=(self.user_role.pk,))
        data = {"email": "user@update.test"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("email"), "user@update.test")

    def test_user_not_owner_update(self):
        """Тестирование прав доступа к обновлению профиля пользователя."""
        url = reverse("user:update_user", args=(self.manager_role.pk,))
        data = {"email": "manager@update.test"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.manager_role.email, "manager@test.test")

    def test_user_delete(self):
        """Тестирование удаления пользователя."""
        url = reverse("user:delete_user", args=(self.user_role.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)

    def test_user_not_owner_delete(self):
        """Тестирование прав доступа к удалению пользователя."""
        url = reverse("user:delete_user", args=(self.manager_role.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.count(), 2)

    def test_user_list(self):
        """Тестирование просмотра списка пользователей."""
        url = reverse("user:users_list")
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                "id": self.user_role.pk,
                "email": self.user_role.email,
                "first_name": None,
                "last_name": None,
                "role": self.user_role.role,
                "is_superuser": False,
                "is_active": True,
            },
            {
                "id": self.manager_role.pk,
                "email": self.manager_role.email,
                "first_name": None,
                "last_name": None,
                "role": self.manager_role.role,
                "is_superuser": False,
                "is_active": True,
            },
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
        self.assertEqual(len(data), 2)
