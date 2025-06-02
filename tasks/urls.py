from django.urls import path

from tasks.apps import TasksConfig
from tasks.views import (CommentCreateAPIView, CommentDestroyAPIView,
                         CommentListAPIView, CommentRetrieveAPIView,
                         CommentUpdateAPIView, TaskCreateAPIView,
                         TaskDestroyAPIView, TaskListAPIView,
                         TaskRetrieveAPIView, TaskUpdateAPIView)

app_name = TasksConfig.name


urlpatterns = [
    path(
        "create/",
        TaskCreateAPIView.as_view(),
        name="create_task",
    ),
    path(
        "tasks/",
        TaskListAPIView.as_view(),
        name="tasks_list",
    ),
    path(
        "retrieve/<int:pk>/",
        TaskRetrieveAPIView.as_view(),
        name="retrieve_task",
    ),
    path(
        "update/<int:pk>/",
        TaskUpdateAPIView.as_view(),
        name="update_task",
    ),
    path(
        "destroy/<int:pk>/",
        TaskDestroyAPIView.as_view(),
        name="destroy_task",
    ),
    path(
        "comment/create/",
        CommentCreateAPIView.as_view(),
        name="create_comment",
    ),
    path(
        "comment/comments/",
        CommentListAPIView.as_view(),
        name="comments_list",
    ),
    path(
        "comment/retrieve/<int:pk>/",
        CommentRetrieveAPIView.as_view(),
        name="retrieve_comment",
    ),
    path(
        "comment/update/<int:pk>/",
        CommentUpdateAPIView.as_view(),
        name="update_comment",
    ),
    path(
        "comment/destroy/<int:pk>/",
        CommentDestroyAPIView.as_view(),
        name="destroy_comment",
    ),
]
