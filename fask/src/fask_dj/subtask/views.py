from django.shortcuts import render, get_object_or_404
from subtask.models import SubTask, SubTaskForm
from dashboard.views import dashboard
from base.views import form_manager, delete_manager
from task.views import task
from task.models import Task
from django.contrib.auth.decorators import login_required

# @login_required
def subtasks(request, show_trashed = False):
    subtasks = SubTask.objects.all()
    context = {'subtasks': subtasks, }
    return render(request, 'subtask/subtasks.html', context)

@login_required
def subtask(request, subtask_id):
    return form_manager(request, subtask_id, SubTask, SubTaskForm, 'task/task.html', subtasks)

@login_required
def subtask_delete(request, subtask_id):
    return delete_manager(request, subtask_id, SubTask, subtasks)

@login_required
def subtask_task(request, subtask_id, task_id, redirect_name):
    if(redirect_name == 'dashboard'):
        tmp_list_view_function = dashboard
    elif(redirect_name == 'task'):
        tmp_list_view_function = task
    
    return form_manager(request, subtask_id, SubTask, SubTaskForm, 'subtask/subtask.html', tmp_list_view_function, default = {'task': get_object_or_404(Task, pk = task_id)})

