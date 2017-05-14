from django.shortcuts import render, get_object_or_404
from .models import Task, TaskForm
from project.models import Project
from dashboard.views import dashboard
from project.views import project
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
def task_project(request, task_id, project_id, redirect_name):
    if(redirect_name == 'dashboard'):
        tmp_list_view_function = dashboard
    elif(redirect_name == 'project'):
        tmp_list_view_function = project
    
    return form_manager(request, task_id, Task, TaskForm, 'task/task.html', tmp_list_view_function, default = {'project': get_object_or_404(Project, pk = project_id)})

