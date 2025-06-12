from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from meetings.models import Meeting
from tasks.models import Task
from users.models import User


class CalendarTestCase(APITestCase):
    """Тесты для вывода календаря."""

    def setUp(self):
        """Окружение для тестов."""
        self.user = User.objects.create(email="user@test.test", role="user")
        self.manager = User.objects.create(email="manager@test.test", role="manager")

        self.client.force_authenticate(user=self.user)

        self.task = Task.objects.create(
            title="Test task",
            description="Test description",
            status="open",
            deadline="2025-06-06",
            author=self.manager,
            task_performer=self.user,
        )
        self.task_for_manager = Task.objects.create(
            title="Test task for manager",
            description="Test description",
            status="open",
            deadline="2025-06-06",
            author=self.manager,
            task_performer=self.manager,
        )
        self.meeting = Meeting.objects.create(
            title="Test meeting",
            date="2025-06-06",
            start_time="10:00:00",
            end_time="11:00:00",
            organizer=self.manager,
        )
        self.meeting.participants.set([self.user, self.manager])

        self.url = reverse("calendar:calendar")

    def test_calendar_day_view_success(self):
        """Тестирует, что календарь на день возвращается."""
        data = {"view": "day", "date": "2025-06-05"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("tasks", response.data)

    def test_calendar_day_view_without_date(self):
        """Тестирует, что календарь на день не возвращается, если не введена дата."""
        data = {"view": "day"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Не указана дата для вывода календаря."
        )

    def test_calendar_view_success(self):
        """Тестирует, что календарь на месяц возвращается."""
        data = {"view": "month", "month": "2025-06"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("month", response.data)

    def test_calendar_month_view_without_date(self):
        """Тестирует, что календарь на месяц не возвращается, если не введена дата."""
        data = {"view": "month"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Не указан месяц для вывода календаря."
        )

    def test_calendar_month_view_invalid_date(self):
        """Тестирует, что календарь на месяц не возвращается, если формат даты неверный."""
        data = {"view": "month", "month": "2025.06"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Неверный формат даты.")

    def test_calendar_default_day_view(self):
        """Тестирует, что возвращается календарь на день, если не введен параметр: view."""
        data = {"date": "2025-06-05"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("tasks", response.data)

    def test_calendar_view_invalid_view(self):
        """Тестирует, что календарь не возвращается, если введен неверный параметр: view."""
        data = {"view": "week", "month": "2025-06"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Введены неверные параметры.")
