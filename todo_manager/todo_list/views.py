from celery import current_app
from celery.result import AsyncResult
from django.db import transaction
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
)
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import (
    ToDoItemCreateForm,
    ToDoItemUpdateForm,
)
from .models import ToDoItem

from .tasks import notify_admin_todo_archived


def index_view(request: HttpRequest) -> HttpResponse:
    todo_items = ToDoItem.objects.all()[:3]
    return render(
        request,
        template_name="todo_list/index.html",
        context={"todo_items": todo_items},
    )


class ToDoListIndexView(ListView):
    template_name = "todo_list/index.html"
    # TODO: custom qs, archived
    queryset = ToDoItem.objects.all()[:3]


class ToDoListView(ListView):
    # model = ToDoItem
    queryset = ToDoItem.objects.filter(archived=False)


class ToDoListDoneView(ListView):
    # TODO: archived qs
    queryset = ToDoItem.objects.filter(done=True).all()


class ToDoDetailView(DetailView):
    # model = ToDoItem
    # TODO: archived qs
    queryset = ToDoItem.objects.filter(archived=False)


class ToDoItemCreateView(CreateView):
    model = ToDoItem
    form_class = ToDoItemCreateForm
    # fields = ("title", "description")


class ToDoItemUpdateView(UpdateView):
    model = ToDoItem
    template_name_suffix = "_update_form"
    form_class = ToDoItemUpdateForm

    # success_url = ...
    #
    # def get_success_url(self):
    #     ...
    # fields = (
    #     "title",
    #     "description",
    #     "done",
    # )


class ToDoItemDeleteView(DeleteView):
    model = ToDoItem
    success_url = reverse_lazy("todo_list:list")

    @transaction.atomic
    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        # notify_admin_todo_archived.delay(todo_id=self.object.pk)
        notify_admin_todo_archived.delay_on_commit(todo_id=self.object.pk)
        return HttpResponseRedirect(success_url)


def task_status(request: HttpRequest) -> HttpResponse:
    task_id = request.GET.get("task_id") or ""
    context = {"task_id": task_id}
    result = AsyncResult(
        task_id,
        app=current_app,
    )
    context.update(
        status=result.status,
        ready=result.ready,
        result=result.result,
    )
    return render(
        request,
        template_name="todo_list/task-status.html",
        context=context,
    )
