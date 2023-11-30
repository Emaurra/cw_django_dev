from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic.edit import CreateView

from survey.models import Answer


class AnswerView(LoginRequiredMixin, CreateView):
    def post(self, request, *args, **kwargs):
        # TODO: Crear un formulario que se encargue de las validaciones
        question_pk = request.POST.get("question_pk")
        answer = request.POST.get("answer")
        if not question_pk or not answer:
            return JsonResponse({"ok": False}, status=400)

        try:
            answer = int(answer)
        except ValueError:
            return JsonResponse({"ok": False}, status=400)

        if answer not in map(lambda x: x[0], Answer.ANSWERS_VALUES):
            return JsonResponse({"ok": False}, status=400)

        user = request.user
        obj, created = Answer.objects.update_or_create(
            author=user,
            question_id=question_pk,
            defaults={
                "value": answer,
            },
        )

        return JsonResponse({"ok": True})
