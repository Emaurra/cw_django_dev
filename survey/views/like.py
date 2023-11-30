from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic.edit import CreateView

from survey.models import Like


class LikeView(LoginRequiredMixin, CreateView):
    def post(self, request, *args, **kwargs):
        question_pk = request.POST.get("question_pk")
        liked = request.POST.get("like")
        if not question_pk or not liked:
            return JsonResponse({"ok": False}, status=400)

        liked = True if liked == "true" else False
        obj, created = Like.objects.update_or_create(
            author=request.user,
            question_id=question_pk,
            defaults={
                "value": liked,
            },
        )

        return JsonResponse({"ok": True})
