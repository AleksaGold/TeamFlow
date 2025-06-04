from django.urls import path

from meetings.apps import MeetingsConfig
from meetings.views import (MeetingCreateAPIView, MeetingDestroyAPIView,
                            MeetingListAPIView, MeetingRetrieveAPIView,
                            MeetingUpdateAPIView, UserMeetingsAPIView)

app_name = MeetingsConfig.name

urlpatterns = [
    path(
        "create/",
        MeetingCreateAPIView.as_view(),
        name="create_meeting",
    ),
    path(
        "meetings/",
        MeetingListAPIView.as_view(),
        name="meetings_list",
    ),
    path(
        "retrieve/<int:pk>/",
        MeetingRetrieveAPIView.as_view(),
        name="retrieve_meeting",
    ),
    path(
        "update/<int:pk>/",
        MeetingUpdateAPIView.as_view(),
        name="update_meeting",
    ),
    path(
        "destroy/<int:pk>/",
        MeetingDestroyAPIView.as_view(),
        name="destroy_meeting",
    ),
    path(
        "user-meetings/",
        UserMeetingsAPIView.as_view(),
        name="user_meetings",
    ),
]
