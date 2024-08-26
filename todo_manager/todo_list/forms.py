from django import forms

from todo_list.models import ToDoItem


class ToDoItemForm(forms.ModelForm):
    class Meta:
        model = ToDoItem
        fields = ("title", "description")

        widgets = {
            "description": forms.Textarea(
                attrs={"cols": 30, "rows": 5},
            ),
        }

        help_texts = {
            "description": "Some useful help text.",
        }
