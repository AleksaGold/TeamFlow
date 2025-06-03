from django.urls import path

from evaluations.apps import EvaluationsConfig
from evaluations.views import (EvaluationCreateAPIView,
                               EvaluationDestroyAPIView, EvaluationListAPIView,
                               EvaluationRetrieveAPIView,
                               EvaluationUpdateAPIView, UserEvaluationsAPIView)

app_name = EvaluationsConfig.name

urlpatterns = [
    path(
        "create/",
        EvaluationCreateAPIView.as_view(),
        name="create_evaluation",
    ),
    path(
        "evaluations/",
        EvaluationListAPIView.as_view(),
        name="evaluations_list",
    ),
    path(
        "retrieve/<int:pk>/",
        EvaluationRetrieveAPIView.as_view(),
        name="retrieve_evaluation",
    ),
    path(
        "update/<int:pk>/",
        EvaluationUpdateAPIView.as_view(),
        name="update_evaluation",
    ),
    path(
        "destroy/<int:pk>/",
        EvaluationDestroyAPIView.as_view(),
        name="destroy_evaluation",
    ),
    path(
        "user-evaluations/",
        UserEvaluationsAPIView.as_view(),
        name="user_evaluations",
    ),
]
