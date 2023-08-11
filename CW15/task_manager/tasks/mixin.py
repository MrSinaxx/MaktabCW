from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404


class TodoOwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        task = self.get_task()
        if task.owner != request.user:
            raise PermissionDenied(
                "You don't have permission to view or edit this Task."
            )
        return super().dispatch(request, *args, **kwargs)

    def get_task(self):
        task_id = self.kwargs.get("task_id")
        return get_object_or_404(Task, id=task_id)
