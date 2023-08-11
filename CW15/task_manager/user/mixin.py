from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class ProfileMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_user():
            raise PermissionDenied(
                "You don't have permission to view or edit this profile."
            )
        return super().dispatch(request, *args, **kwargs)

    def get_user(self):
        raise NotImplementedError(
            "Define get_user in the view to retrieve the user instance."
        )


from django.shortcuts import get_object_or_404


class ObjectGetUpdateMixin:
    model = None
    form_class = None

    def get_object(self, *args, **kwargs):
        obj_id = self.kwargs.get("id")
        if not obj_id or not self.model:
            raise ValueError("Model not defined or ID not provided.")
        return get_object_or_404(self.model, id=obj_id)

    def update_object(self, request):
        obj = self.get_object()
        form = self.form_class(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return True, form
        return False, form
