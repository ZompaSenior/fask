from django.shortcuts import render, get_object_or_404
from .models import Task, TaskForm
from project.models import Project

from dashboard.views import dashboard, task_calendar

from base.views import form_manager, delete_manager
from django.contrib.auth.decorators import login_required

# @login_required
def tasks(request, show_trashed = False):
    tasks = Task.objects.all()
    context = {'tasks': tasks, }
    return render(request, 'task/tasks.html', context)

@login_required
def task(request, task_id):
    return form_manager(request, task_id, Task, TaskForm, 'task/task.html', tasks)

@login_required
def task_delete(request, task_id):
    return delete_manager(request, task_id, Task, dashboard)

@login_required
def task_project(request, task_id, project_id, redirect_name):
    if redirect_name == 'dashboard':
        redirect_obj = dashboard
    else:
        redirect_obj = task_calendar
        
    return form_manager(request, task_id, Task, TaskForm, 'task/task.html', redirect_obj, default = {'project': get_object_or_404(Project, pk = project_id)})

