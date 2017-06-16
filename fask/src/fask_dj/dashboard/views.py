from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from project.models import Project, ProjectState

def dashboard(request):
    template = loader.get_template('dashboard/dashboard.html')

    values = ('false', 'true')
    
    tmp_show_completed = request.GET.get('show_completed')
    try:
        index = values.index(tmp_show_completed.lower())
        tmp_show_completed = bool(index)
    except ValueError:
        tmp_show_completed = False
    except AttributeError:
        tmp_show_completed = False
    
    tmp_filter_supervisor = request.GET.get('filter_supervisor')
    try:
        index = values.index(tmp_filter_supervisor.lower())
        tmp_filter_supervisor = bool(index)
    except ValueError:
        tmp_filter_supervisor = False
    except AttributeError:
        tmp_filter_supervisor = False
    
    if(tmp_show_completed and not tmp_filter_supervisor):
        projects = Project.objects.all()
    else:
        if(tmp_show_completed):
            projects = Project.objects.filter(supervisor__username=request.user.username)
        else:
            if(tmp_filter_supervisor):
                projects = Project.objects.filter(supervisor__username=request.user.username).exclude(state__description='99 - Completato')
            else:
                projects = Project.objects.exclude(state__description='99 - Completato')
        
    context = {'projects': projects, }
    return HttpResponse(template.render(context, request))