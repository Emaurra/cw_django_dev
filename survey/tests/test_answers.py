import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse

from survey.models import Question


@pytest.mark.django_db
class TestCreateQuestion:
    def test_create_question(self, client) -> None:
        assert Question.objects.count() == 0
        username = "testUser"
        password = "testpass"
        user = get_user_model().objects.create_user(
            username=username,
            password=password,
        )

        logged_in = client.login(username=username, password=password)
        assert logged_in
        url = reverse("survey:question-create")
        question_title = "soy pregunta"
        question_description = "soy una descripcion"
        response = client.post(
            url,
            {"title": question_title, "description": question_description},
        )

        question = Question.objects.get(pk=1)
        assert question.title == question_title
        assert question.description == question_description
