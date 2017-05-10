# -*- coding: Cp1252 -*-
from django.shortcuts import get_object_or_404, render, redirect
"""from django.db.models import Max
from django.db.models.aggregates import Count"""
from base.models import FaskObject, EditInfo

# from django.contrib.auth.decorators import login_required

def form_manager(request, object_id, object_model, form_model, template_name, list_view_function, show_trashed = 'False', default = None):
    
    if(len(object_id) > 0 and object_id != '0' and object_id != '_'):
        tmp_object = get_object_or_404(object_model, pk = object_id)
    else:
        tmp_object = None
        
    if request.method == "POST":
        
        """
        if(issubclass(object_model, RevInfo)):
            tmp_name = request.POST.get('name', '')
            if(tmp_object):
                tmp_new_revision = object_model.objects.filter(name = tmp_name).aggregate(Max('revision'))['revision__max'] + 1
            else:
                tmp_new_revision = 1
            
            tmp_object = None
        """
        form = form_model(request.POST, request.FILES, instance = tmp_object)
        
        if(issubclass(object_model, EditInfo)):
            form.set_user(str(request.user))
        
        """
        if(issubclass(object_model, RevInfo)):
            form.set_revision(tmp_new_revision)
        """
        
        if form.is_valid():
            form.save()
            print(list_view_function.__name__)
            if(list_view_function.__code__.co_argcount == 1):
                return redirect('/%s/' % (list_view_function.__name__,))
                # return list_view_function(request)
            else:
                return redirect('/%s/%s/' % (list_view_function.__name__, show_trashed))
                # return list_view_function(request, show_trashed)
        else:
            print('Invalid')
    else:
        form = form_model(instance = tmp_object)
        
        if(default == None):
            pass
        else:
            for key, value in default.items():
                getattr(form, key)(value)
            
    context = {form_model.__name__.lower: tmp_object, 'form': form, 'show_trashed': show_trashed }
    
    return render(request, template_name, context)

def delete_manager(request, object_id, object_model, list_view_function, show_trashed = False):
    if(len(object_id) > 0 and object_id != '0' and object_id != '_'):
        tmp_object = get_object_or_404(object_model, pk = object_id)
        if(issubclass(object_model, EditInfo)):
            tmp_object.set_user(str(request.user))

        tmp_object.delete()
    
    return list_view_function(request, show_trashed)

def restore_manager(request, object_id, object_model, list_view_function, show_trashed = False):
    if(len(object_id) > 0 and object_id != '0' and object_id != '_'):
        tmp_object = get_object_or_404(object_model, pk = object_id)

        if(issubclass(object_model, EditInfo)):
            tmp_object.set_user(str(request.user))

        tmp_object.restore()
        
    return list_view_function(request, show_trashed)

"""
# @login_required
def groups(request, show_trashed = False):
    groups = Group.objects.order_by('order_index')
    context = {'groups': groups, 'show_trashed': show_trashed }
    return render(request, 'spal/groups.html', context)

# @login_required
def group(request, group_id, show_trashed = False):
    return form_manager(request, group_id, Group, GroupForm, 'spal/group.html', groups, show_trashed)

# @login_required
def group_delete(request, group_id, show_trashed = False):
    return delete_manager(request, group_id, Group, groups, show_trashed)

# @login_required
def atxxxxs(request, show_trashed = False):
    atxxxxs = Atxxxx.objects.order_by('owning_group__order_index', 'name')
    context = {'atxxxxs': atxxxxs, 'show_trashed': show_trashed }
    return render(request, 'spal/atxxxxs.html', context)

# @login_required
def atxxxx(request, atxxxx_id, show_trashed = False):
    return form_manager(request, atxxxx_id, Atxxxx, AtxxxxForm, 'spal/atxxxx.html', atxxxxs, show_trashed)

# @login_required
def atxxxx_delete(request, atxxxx_id, show_trashed = False):
    return delete_manager(request, atxxxx_id, Atxxxx, atxxxxs, show_trashed)

# @login_required
def select_atxxxx(request, group_id, show_trashed = False):
    atxxxxs = Atxxxx.objects.filter(owning_group=0).order_by('name')
    context = {'atxxxxs': atxxxxs, 'group_id': group_id }
    return render(request, 'spal/select_atxxxx.html', context)
"""


