from django.shortcuts import render
from .models import Project, ProjectForm
from base.views import form_manager, delete_manager
from django.contrib.auth.decorators import login_required

# @login_required
def projects(request, show_trashed = False):
    projects = Project.objects.all()
    context = {'projects': projects, }
    return render(request, 'project/projects.html', context)

@login_required
def project(request, project_id):
    return form_manager(request, project_id, Project, ProjectForm, 'project/project.html', projects)

@login_required
def project_delete(request, project_id):
    return delete_manager(request, project_id, Project, projects)

