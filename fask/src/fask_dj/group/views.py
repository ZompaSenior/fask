from django.shortcuts import render
from .models import Group, GroupForm
from base.views import form_manager, delete_manager
from django.contrib.auth.decorators import login_required

# @login_required
def groups(request, show_trashed = False):
    groups = Group.objects.all()
    context = {'groups': groups}
    return render(request, 'group/groups.html', context)

@login_required
def group(request, group_id):
    return form_manager(request, group_id, Group, GroupForm, 'group/group.html', groups)

@login_required
def group_delete(request, group_id):
    return delete_manager(request, group_id, Group, GroupForm)

