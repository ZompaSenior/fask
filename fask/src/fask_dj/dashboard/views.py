# -*- coding: Cp1252 -*-

import datetime
import calendar

from project.models import Project

from task.models import Task


from django.utils import timezone
from django.template import loader
from django.shortcuts import render
from django.urls.base import reverse
from django.http import HttpResponse, JsonResponse




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
                                        if task.due_to == date.date()]
                