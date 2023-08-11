from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):  # Inherit from ModelForm
    class Meta:
        model = Todo
        fields = ["title", "description", "is_completed"]  # Removed 'user'
