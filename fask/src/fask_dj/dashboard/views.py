from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from project.models import Project, ProjectState

def dashboard(request, show_completed = 'false'):
    template = loader.get_template('dashboard/dashboard.html')
    
    try:
        values = ('false', 'true')
        index = values.index(show_completed.lower())
        tmp_show_completed = bool(index)
    except ValueError:
        tmp_show_completed = False
    
    if(tmp_show_completed):
        projects = Project.objects.all()
    else:
        projects = Project.objects.exclude(state__description='99 - Completato')
        
    context = {'projects': projects, 'show_completed': tmp_show_completed}
    return HttpResponse(template.render(context, request))