class AuthorValidatorMixin:
    def get_queryset(self, *args, **kwargs):
        return (
            super().get_queryset(*args, **kwargs).filter(author_id=self.request.user.id)
        )

    """def dispatch(self, request, *args, **kwargs):
        print("=>>>>>", request, flush=True)
        obj = self.get_object()
        if obj and obj.author_id != self.request.user.id:
            return HttpResponseForbidden()

        return super().dispatch(request, *args, **kwargs)
    """
