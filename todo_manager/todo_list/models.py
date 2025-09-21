from django.db import models
from django.urls import reverse


class ToDoItemQuerySet(models.QuerySet):

    def active(self):
        return self.filter(archived=False)

    def done(self):
        return self.filter(done=True)


class ToDoItem(models.Model):

    class Meta:
        ordering = ("id", )
        verbose_name = "ToDo Item"

    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=False)
    done = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    objects = ToDoItemQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse(
            "todo_list:detail",
            kwargs={"pk": self.pk},
        )

    def __str__(self):
        return self.title

