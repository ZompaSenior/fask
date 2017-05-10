from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from project.models import Project

def dashboard(request):
    template = loader.get_template('dashboard/dashboard.html')
    projects = Project.objects.all()
    context = {'projects': projects, }
    return HttpResponse(template.render(context, request))