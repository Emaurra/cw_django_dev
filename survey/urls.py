from django.urls import path

from survey.views.answer import AnswerView
from survey.views.like import LikeView
from survey.views.question import (
    QuestionCreateView,
    QuestionDeleteView,
    QuestionListView,
    QuestionUpdateView,
)

urlpatterns = [
    path("", QuestionListView.as_view(), name="question-list"),
    path("question/add/", QuestionCreateView.as_view(), name="question-create"),
    path("question/edit/<int:pk>", QuestionUpdateView.as_view(), name="question-edit"),
    path(
        "question/delete/<int:pk>", QuestionDeleteView.as_view(), name="question-delete"
    ),
    path("question/answer", AnswerView.as_view(), name="question-answer"),
    path("question/like", LikeView.as_view(), name="question-like"),
]
