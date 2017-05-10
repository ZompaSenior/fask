from django.shortcuts import render
from .models import Task, TaskForm
from base.views import form_manager, delete_manager

# @login_required
def tasks(request, show_trashed = False):
    tasks = Task.objects.all()
    context = {'tasks': tasks, }
    return render(request, 'task/tasks.html', context)

# @login_required
def task(request, task_id):
    return form_manager(request, task_id, Task, TaskForm, 'task/task.html', tasks)

# @login_required
def task_delete(request, project_id):
    return delete_manager(request, project_id, Task, tasks)

# @login_required
def task_project(request, task_id, project_id):
    return form_manager(request, task_id, Task, TaskForm, 'task/task.html', tasks, default = {'set_project': project_id})

