from django import forms

from todo_list.models import ToDoItem


class ToDoItemSearchForm(forms.Form):
    search = forms.CharField(
        label='Search todo items',
        required=False,
    )


class ToDoItemCreateForm(forms.ModelForm):
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


class ToDoItemUpdateForm(forms.ModelForm):
    class Meta(ToDoItemCreateForm.Meta):
        fields = (
            "title",
            "description",
            "done",
        )
