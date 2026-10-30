from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import RegisterForm, TaskForm
from .models import Task


def visible_tasks(user):
    """Админ (is_staff) видит все задачи, обычный пользователь — только свои."""
    tasks = Task.objects.select_related("user")
    return tasks if user.is_staff else tasks.filter(user=user)


def register(request):
    if request.user.is_authenticated:
        return redirect("task_list")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Аккаунт создан, добро пожаловать!")
        return redirect("task_list")
    return render(request, "tasks/register.html", {"form": form})


@login_required
def task_list(request):
    tasks = visible_tasks(request.user)
    return render(request, "tasks/task_list.html", {"tasks": tasks})


@login_required
def task_create(request):
    form = TaskForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        messages.success(request, "Задача добавлена")
        return redirect("task_list")
    return render(request, "tasks/task_form.html", {"form": form, "title": "Новая задача"})


@login_required
def task_update(request, pk):
    task = get_object_or_404(visible_tasks(request.user), pk=pk)
    form = TaskForm(request.POST or None, instance=task)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Изменения сохранены")
        return redirect("task_list")
    return render(request, "tasks/task_form.html", {"form": form, "title": "Редактирование"})


@login_required
@require_POST
def task_toggle(request, pk):
    task = get_object_or_404(visible_tasks(request.user), pk=pk)
    task.is_done = not task.is_done
    task.save(update_fields=["is_done"])
    return redirect("task_list")


@login_required
def task_delete(request, pk):
    task = get_object_or_404(visible_tasks(request.user), pk=pk)
    if request.method == "POST":
        task.delete()
        messages.success(request, "Задача удалена")
        return redirect("task_list")
    return render(request, "tasks/task_confirm_delete.html", {"task": task})
