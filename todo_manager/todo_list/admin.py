from django.contrib import admin

from todo_list.models import ToDoItem


@admin.register(ToDoItem)
class ToDoItemAdmin(admin.ModelAdmin):
    list_display = "id", "title", "description", "visible", "done"
    list_display_links = "id", "title"

    def visible(self, obj: ToDoItem) -> bool:
        return not obj.archived

    visible.boolean = True
