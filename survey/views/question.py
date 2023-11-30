from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import (
    Case,
    Count,
    F,
    FilteredRelation,
    OuterRef,
    Q,
    Subquery,
    Value,
    When,
)
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from survey.mixins.author_validator import AuthorValidatorMixin
from survey.models import Answer, Like, Question


def calculate_ranking(answers, liked, not_liked, is_today):
    """Retorna el puntaje calculado para el ranking de las preguntas

    - Cada respuesta suma 10 puntos al ranking
    - Cada like suma 5 puntos al ranking
    - Cada dislike resta 3 puntos al ranking
    - Las preguntas del día de hoy, tienen un extra de 10 puntos

    Args:
        answers: Cantidad de respuestas
        liked: Cantidad de "Me gusta"
        not_liked: Cantidad de "No me gusta"
        is_today: 0 si no es de hoy y 1 si fue creada hoy

    Returns:
        int: ranking calulado
    """
    return answers * 10 + liked * 5 - not_liked * 3 + is_today * 10


class QuestionListView(LoginRequiredMixin, ListView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["answers"] = list(map(lambda x: x[0], Answer.ANSWERS_VALUES[1:]))
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        now = datetime.now()

        return (
            qs.annotate(
                answered=FilteredRelation(
                    "answers", condition=Q(answers__author_id=user.id)
                )
            )
            .annotate(
                liked=FilteredRelation("likes", condition=Q(likes__author__id=user.id))
            )
            .annotate(
                ranking=Subquery(
                    Question.objects.filter(pk=OuterRef("pk"))
                    .annotate(today_points=Case(When(created=now, then=1), default=0))
                    .annotate(
                        liked=FilteredRelation(
                            "likes",
                            condition=Q(likes__author__id=user.id)
                            & Q(likes__value=True),
                        ),
                        notliked=FilteredRelation(
                            "likes",
                            condition=Q(likes__author__id=user.id)
                            & Q(likes__value=False),
                        ),
                    )
                    .annotate(
                        answered=calculate_ranking(
                            Count("id"),
                            Count("liked"),
                            Count("notliked"),
                            F("today_points"),
                        )
                    )
                    .values("answered")
                )
            )
            .values(
                "description",
                "title",
                "id",
                "ranking",
                answered=F("answered__value"),
                liked=F("liked__value"),
                author_name=F("author__username"),
                author_pk=F("author__pk"),
            )
        ).order_by("-ranking")


class QuestionCreateView(LoginRequiredMixin, AuthorValidatorMixin, CreateView):
    model = Question
    fields = ["title", "description"]
    redirect_url = ""
    success_url = reverse_lazy("survey:question-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "create"
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)


class QuestionUpdateView(LoginRequiredMixin, AuthorValidatorMixin, UpdateView):
    model = Question
    fields = ["title", "description"]
    template_name = "survey/question_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "edit"
        return context


class QuestionDeleteView(LoginRequiredMixin, AuthorValidatorMixin, DeleteView):
    model = Question
    success_url = reverse_lazy("survey:question-list")
