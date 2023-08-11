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
