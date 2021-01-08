# -*- coding: Cp1252 -*-

import json
import datetime
import calendar

from project.models import Project, ProjectState
from task.models import Task, TaskPriority, TaskProgression
from subtask.models import SubTask
from group.models import Group

from django.db import transaction
from django.utils import timezone
from django.template import loader
from django.urls.base import reverse
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse






def handle_import_tag_file(f):
    
    """Decodifica il contenuto del file da importare in utf-8.
    
    Args:
        f (file): il buffer da decodificare
    
    Returns:
        str: il contenuto decodificato
        
    """
    
    contenuto = f.read().decode("utf-8")
    
    return contenuto


def dashboard(request):
    template = loader.get_template('dashboard/dashboard.html')
    projects = Project.objects.all()
    context = {'projects': projects, 'user': request.user.username}
    return HttpResponse(template.render(context, request))


def task_calendar(request):
    context = {
        'month'      : (timezone.localtime(timezone.now())).strftime("%B"), 
    }
    return render(request, 'dashboard/task_calendar.html', context)

def task_calendar_details_request(request, select_day, negative = 'False'):
    head_list = []
    cell_list = []
    select_day = int(select_day)
    if(negative != 'False'):
        select_day = select_day*(-1)
    date = timezone.localtime(timezone.now())
    date += datetime.timedelta(days = select_day)
    i = 0
    task_list = [task for task in Task.objects.filter(due_to__year = date.year).filter(due_to__week = date.isocalendar()[1]).exclude(progression__description__startswith= '99').order_by('-priority')]
    month = date.strftime("%B")
    date -= datetime.timedelta(days=date.weekday())
    for i in range(7):
        head_list.append(f"""<th>{calendar.day_name[date.weekday()]}: {date.day}</th>""")
        cell_list.append(f"""<td>{"".join(get_task_calendar_cell(date, task_list))}</td>""") 
        date += datetime.timedelta(days= 1)
    context = {
            'month'      : month,    
            'head_list'  : head_list,
            'cell_list'  : cell_list,
            'select_day' : select_day
        }
    return JsonResponse(context)

def get_task_calendar_cell(date, task_list):
    return [ f"""<div id="task_{task.description}_{task.assigned_to}">
                <div>
                    <button type="button" class="btn btn-default" data-toggle="tooltip" data-placement="bottom" title="{ task.annotation }" onclick="location.href='{reverse("task_project", args = [task.id, task.project.id, 'task_calendar'])}';">Task : {task.description}</button>
                </div>
                <div>
                    <h4>Progetto: {task.project.description}</h4>
                    <h5>Assegnato: {task.assigned_to}</h5>
                    <h5>Progresso: {task.progression}</h5>
                    <h5>Priorità: {task.priority}</h5>
                </div>
                </div>""" 
                                for task in task_list 
                                        if task.due_to.date() == date.date()]
                
                
                
def import_export_page(request):
    return render(request, 'dashboard/import_export_panel.html', {})


def export_fask(request):
    tmp_dict     = {}
    project_list = []
    projects     = Project.objects.all()
   
    
    for project in projects:
        project_dict = model_to_dict(project, fields=['description', 'annotation', 'creation_user', 'edit_user'])
        project_dict['state']          = project.state.description                              if project.state            else "None"
        project_dict['supervisor']     = project.supervisor.username                            if project.supervisor       else "None"    
        project_dict['group']          = project.group.description                              if project.group            else "None" 
        project_dict['creation_date']  = project.creation_date.strftime("%d/%m/%Y %H:%M:%S")    if project.creation_date    else "None"
        project_dict['edit_date']      = project.edit_date.strftime("%d/%m/%Y %H:%M:%S")        if project.edit_date        else "None"
        project_dict['start_date']     = project.start_date.strftime("%d/%m/%Y %H:%M:%S")       if project.start_date       else "None"
        project_dict['end_date']       = project.end_date.strftime("%d/%m/%Y %H:%M:%S")         if project.end_date         else "None"

        task_list = []
        
        for task in project.task_project_owner.all():
            task_dict = model_to_dict(task, fields=['description', 'annotation', 'creation_user', 'edit_user'])
            task_dict['priority']       = task.priority.description                         if task.priority        else "None"                    
            task_dict['progression']    = task.progression.description                      if task.progression     else "None"
            task_dict['assigned_to']    = task.assigned_to.username                         if task.assigned_to     else "None"
            task_dict['due_to']         = task.due_to.strftime("%d/%m/%Y %H:%M:%S")         if task.due_to          else "None"
            task_dict['completed_on']   = task.completed_on.strftime("%d/%m/%Y %H:%M:%S")   if task.completed_on    else "None"
            task_dict['creation_date']  = task.creation_date.strftime("%d/%m/%Y %H:%M:%S")  if task.creation_date   else "None"
            task_dict['edit_date']      = task.edit_date.strftime("%d/%m/%Y %H:%M:%S")      if task.edit_date       else "None"
            
            subtask_list = []
            
            for subtask in task.task_owner.all():
                subtask_dict = model_to_dict(subtask, fields=['description', 'annotation', 'creation_user', 'edit_user', 'completed'])
                subtask_dict['creation_date']  = subtask.creation_date.strftime("%d/%m/%Y %H:%M:%S")    if subtask.creation_date    else "None"
                subtask_dict['edit_date']      = subtask.edit_date.strftime("%d/%m/%Y %H:%M:%S")        if subtask.edit_date        else "None"
                subtask_dict['completed_on']   = subtask.completed_on.strftime("%d/%m/%Y %H:%M:%S")     if subtask.completed_on     else "None"
                
                subtask_list.append(subtask_dict)
                subtask_dict = {}
                
            task_dict['subtasks'] = subtask_list
            task_list.append(task_dict)
            task_dict = {}
            
        project_dict['tasks'] = task_list
        project_list.append(project_dict)
        project_dict = {}
    
    tmp_dict['projects'] = project_list
    ts = timezone.localtime(timezone.now()).strftime("%d_%m_%Y-%H:%M:%S")
    tmp_dict['export_date'] = ts
    json_str = json.dumps(tmp_dict, indent = 2)
    response = HttpResponse(json_str, content_type='text/json')
    response['Content-Disposition'] = f'attachment; filename="fask_export_{ts}.json"'
    
    return response

@transaction.atomic
def import_fask(request):

    warning_list    = []
    error_list      = []
    tmp_import_mdoe = request.POST.get('import_mode', 'append')

    try:
        with transaction.atomic():
            if(request.FILES):
                if(request.FILES.get('file_to_import', '')):
                    try:
                        with transaction.atomic():
                            file_content = handle_import_tag_file(request.FILES['file_to_import'])
                    except Exception as e:
                        raise ValueError(f"file is corrupt, Exception: {e}") 
                    try:
                        with transaction.atomic():
                            file_fask = json.loads(file_content)
                    except Exception as e:
                        raise ValueError(f"file import is corrupt, ecx: {e} \n\n file content: {file_content} ")
                    
                else:
                    raise ValueError(f"lista file vuota, trovati file ma non file_to_import")
            else:
                raise ValueError(f"lista file vuota")    
            
            if(tmp_import_mdoe == 'reset'):
                projects = Project.objects.all()
                for project in projects:
                    for task in project.task_project_owner.all():
                        for subtask in task.task_owner.all():
                            subtask.delete()
                        task.delete()
                    project.delete()
                project_name_list   = []
                task_name_list      = []
                subtask_name_list   = []
            else:
                project_name_list   = [project.description  for project in Project.objects.all()]
                task_name_list      = [task.description     for task in Task.objects.all()]
                subtask_name_list   = [subtask.description  for subtask in SubTask.objects.all()]
            
            for project_dict in file_fask['projects']:
                
                if project_dict['description'] in project_name_list:
                    projects = Project.objects.filter(description = project_dict['description']).all()
                    
                    if len(projects) == 0 or len(projects) > 1:
                        error_list.append(f"Incongruenza Database elemento {project_dict['description']} non trovato o trovato multiplo")
                        continue
                    project = projects[0]
                else:
                    project = Project()
                
                project.description     = project_dict['description']
                project.annotation      = project_dict['annotation']
                project.edit_user       = project_dict['edit_user']
                project.creation_user   = project_dict['creation_user']
                project.start_date      = datetime.datetime.strptime(project_dict['start_date'], "%d/%m/%Y %H:%M:%S")       if project_dict['start_date']       != "None" else None
                project.end_date        = datetime.datetime.strptime(project_dict['end_date'], "%d/%m/%Y %H:%M:%S")         if project_dict['end_date']         != "None" else None
                project.creation_date   = datetime.datetime.strptime(project_dict['creation_date'], "%d/%m/%Y %H:%M:%S")    if project_dict['creation_date']    != "None" else None
                project.edit_date       = datetime.datetime.strptime(project_dict['edit_date'], "%d/%m/%Y %H:%M:%S")        if project_dict['edit_date']        != "None" else None
            
                states = ProjectState.objects.filter(description = project_dict['state']) 
                if (len(states) == 0 or len(states)> 1) and project_dict['state'] != "None":
                    error_list.append(f"Incongruenza Database elemento Stato:{project_dict['state']}, Project: {project_dict['description']} non trovato o trovato multiplo")
                    continue
                elif project_dict['state'] == "None":
                    project.state = None
                else:
                    project.state = states[0]
                
                supervisors = User.objects.filter(username = project_dict['supervisor'])     
                if (len(supervisors) == 0 or len(supervisors)> 1) and project_dict['supervisor'] != "None":
                    error_list.append(f"Incongruenza Database elemento Stato:{project_dict['supervisor']}, Project: {project_dict['description']} non trovato o trovato multiplo")
                    continue
                elif project_dict['supervisor'] == "None":
                    project.supervisor = None
                else:
                    project.supervisor = supervisors[0]
                    
                groups = Group.objects.filter( description = project_dict['group'])     
                if (len(groups) == 0 or len(groups)> 1) and project_dict['group'] != "None":
                    error_list.append(f"Incongruenza Database elemento Gruppo:{project_dict['group']}, Project: {project_dict['description']} non trovato o trovato multiplo")
                    continue
                elif project_dict['group'] == "None":
                    project.group = None
                else:
                    project.group = groups[0]
                    
                project.save()        
                
                for task_dict in project_dict['tasks']:
                    if task_dict['description'] in task_name_list:
                        tasks = Task.objects.filter(description = task_dict['description']).all()
                    
                        if len(tasks) == 0 or len(tasks) > 1:
                            error_list.append(f"Incongruenza Database  Task: {task_dict['description']}, Project:{project_dict['description']} non trovato o trovato multiplo")
                            continue
                        task = tasks[0]
                    else:
                        task = Task()
                        
                    task.project         = project
                    task.description     = task_dict['description']
                    task.annotation      = task_dict['annotation']
                    task.edit_user       = task_dict['edit_user']
                    task.creation_user   = task_dict['creation_user']
                    task.completed_on    = datetime.datetime.strptime(task_dict['completed_on'], "%d/%m/%Y %H:%M:%S")   if task_dict['completed_on']    != "None" else None
                    task.due_to          = datetime.datetime.strptime(task_dict['due_to'], "%d/%m/%Y %H:%M:%S")         if task_dict['due_to']          != "None" else None
                    task.creation_date   = datetime.datetime.strptime(task_dict['creation_date'], "%d/%m/%Y %H:%M:%S")  if task_dict['creation_date']   != "None" else None
                    task.edit_date       = datetime.datetime.strptime(task_dict['edit_date'], "%d/%m/%Y %H:%M:%S")      if task_dict['edit_date']       != "None" else None
                
                    priorities = TaskPriority.objects.filter(description = task_dict['priority']) 
                    if (len(priorities) == 0 or len(priorities)> 1) and task_dict['priority'] != "None":
                        error_list.append(f"Incongruenza Database elemento Priority:{task_dict['priority']}, Task: {task_dict['description']}, Project: {project_dict['description']} non trovato o trovato multiplo")
                        continue
                    elif task_dict['priority'] == "None":
                        task.priority = None
                    else:
                        task.priority = priorities[0]
                    
                    assigned_to = User.objects.filter(username = task_dict['assigned_to'])     
                    if (len(assigned_to) == 0 or len(assigned_to)> 1) and task_dict['assigned_to'] != "None":
                        error_list.append(f"Incongruenza Database elemento User Assegnato:{task_dict['assigned_to']}, Task: {task_dict['description']}, Project: {project_dict['description']} non trovato o trovato multiplo")
                        continue
                    elif task_dict['assigned_to'] == "None":
                        task.assigned_to = None
                    else:
                        task.assigned_to = assigned_to[0]
                        
                    progressiones = TaskProgression.objects.filter(description = task_dict['progression'])     
                    if (len(progressiones) == 0 or len(progressiones)> 1) and task_dict['progression'] != "None":
                        error_list.append(f"Incongruenza Database elemento Progression:{task_dict['progression']}, Task: {task_dict['description']}, Project: {project_dict['description']} non trovato o trovato multiplo")
                        continue
                    elif task_dict['progression'] == "None":
                        task.progression = None
                    else:
                        task.progression = progressiones[0]
                        
                    task.save()   
                    
                    for subtask_dict in task_dict['subtasks']:
                        if subtask_dict['description'] in subtask_name_list:
                            subtasks = SubTask.objects.filter(description = subtask_dict['description']).all()
                        
                            if len(subtasks) == 0 or len(subtasks) > 1:
                                error_list.append(f"Incongruenza Database SubTask:{subtask_dict['description']}, Task: {task_dict['description']}, Project:{project_dict['description']} non trovato o trovato multiplo")
                                continue
                            subtask = subtasks[0]
                        else:
                            subtask = SubTask()
                            
                        subtask.task            = task
                        subtask.description     = subtask_dict['description']
                        subtask.annotation      = subtask_dict['annotation']
                        subtask.edit_user       = subtask_dict['edit_user']
                        subtask.completed       = subtask_dict['completed']
                        subtask.creation_user   = subtask_dict['creation_user']
                        subtask.completed_on    = datetime.datetime.strptime(subtask_dict['completed_on'], "%d/%m/%Y %H:%M:%S") if subtask_dict['completed_on']   != "None" else None
                        subtask.creation_date   = datetime.datetime.strptime(subtask_dict['creation_date'], "%d/%m/%Y %H:%M:%S")if subtask_dict['creation_date']  != "None" else None
                        subtask.edit_date       = datetime.datetime.strptime(subtask_dict['edit_date'], "%d/%m/%Y %H:%M:%S")    if subtask_dict['edit_date']      != "None" else None
                    
                        subtask.save()   
                    
            if len(error_list)>0:
                raise ValueError("Riscontrati i Seguenti errori")
            
            return redirect(reverse("dashboard", args = []))  
        
    except ValueError as e:
        context={
            "succes": False,
            "title": "Import Fask(Projects,Tasks,SubTasks)",
            "error_text": f"{e}",
            "error_list":error_list,
            "return_url": reverse('import_export_page', args = []) 
        }
        
        return render(request, 'dashboard/alter.html' , context)  

    
