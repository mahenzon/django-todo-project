from django.db import models
from django.urls import reverse


class ToDoItem(models.Model):

    class Meta:
        ordering = ("id", )
        verbose_name = "ToDo Item"

    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=False)
    done = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse(
            "todo_list:detail",
            kwargs={"pk": self.pk},
        )

    def __str__(self):
        return self.title
