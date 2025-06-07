from calendar import monthrange
from datetime import datetime

from django.utils.dateparse import parse_date
from rest_framework.response import Response
from rest_framework.views import APIView

from meetings.models import Meeting
from meetings.serializers import MeetingSerializer
from tasks.models import Task
from tasks.serializers import TaskSerializer


class CalendarAPIView(APIView):
    """
    Представление для отображения задач и встреч в виде календаря.

    Поддерживает два режима отображения:
    - 'day': возвращает список задач и встреч на конкретную дату (параметр `date` обязателен);
    - 'month': возвращает задачи и встречи, сгруппированные по дням за указанный месяц (параметр `month` в формате YYYY-MM обязателен).

    GET-параметры:
        - view (str): 'day' или 'month' (по умолчанию 'day')
        - date (str): дата в формате 'YYYY-MM-DD' (только для 'day')
        - month (str): месяц в формате 'YYYY-MM' (только для 'month')

    Возвращает HTTP 400, если обязательные параметры отсутствуют или некорректны.
    """

    def get(self, request):
        user = request.user
        view_type = request.query_params.get("view", "day")

        if view_type == "day":
            date_str = request.query_params.get("date")
            if not date_str:
                return Response(
                    {"error": "Не указана дата для вывода календаря."}, status=400
                )
            date = parse_date(date_str)

            meetings = Meeting.objects.filter(participants=user, date=date)
            tasks = Task.objects.filter(task_performer=user, deadline=date)

            return Response(
                {
                    "date": date_str,
                    "meetings": MeetingSerializer(meetings, many=True).data,
                    "tasks": TaskSerializer(tasks, many=True).data,
                }
            )
        elif view_type == "month":
            month_str = request.query_params.get("month")
            if not month_str:
                return Response(
                    {"error": "Не указан месяц для вывода календаря."}, status=400
                )

            try:
                year, month = map(int, month_str.split("-"))
                start_date = datetime(year, month, 1).date()
                end_date = datetime(year, month, monthrange(year, month)[1]).date()
            except ValueError:
                return Response({"error": "Неверный формат даты."}, status=400)
            meetings = Meeting.objects.filter(
                participants=user, date__range=(start_date, end_date)
            )
            tasks = Task.objects.filter(
                task_performer=user, deadline__range=(start_date, end_date)
            )

            result = {}
            for day in range(1, monthrange(year, month)[1] + 1):
                day_date = datetime(year, month, day).date()
                result[str(day_date)] = {
                    "meetings": MeetingSerializer(
                        meetings.filter(date=day_date), many=True
                    ).data,
                    "tasks": TaskSerializer(
                        tasks.filter(deadline=day_date), many=True
                    ).data,
                }

            return Response({"month": month_str, "calendar": result})
        return Response({"error": "Введены неверные параметры."}, status=400)
