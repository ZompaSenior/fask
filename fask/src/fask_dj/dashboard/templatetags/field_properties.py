# -*- coding: Cp1252 -*-
"""
Contiene funzioni da usare come TAG nei template..
"""
__author__ = "ZOMPARELLIL"
__version__ = "0.1.0"
__license__ = "Spal Automotive, 2018"

import re
from builtins import str
from django import template
from . import spal_helper as sh
from django.middleware import csrf
from django.urls.base import reverse
from django.apps.registry import apps
from django.utils.html import format_html
from django.core.exceptions import FieldError
from django.utils.safestring import mark_safe
from django.contrib.staticfiles.templatetags.staticfiles import static






register = template.Library()

def escape_args(original_function):
    def new_function(*args, **kwargs):
        args = [arg.replace('{', '{{').replace('}', '}}') if isinstance(arg, str) else arg for arg in args]
        return original_function(*args, **kwargs)
        
    return new_function

def print_result(original_function):
    def new_function(*args, **kwargs):
        returned_value = original_function(*args, **kwargs)
        return returned_value
        
    return new_function


@register.simple_tag
def get_title_from_class(target_class):
    try:
        return ' '.join(re.sub('(?!^)([A-Z][a-z]+)', r' \1', str(target_class.__name__)).split())
    except AttributeError:
        return ' '.join(re.sub('(?!^)([A-Z][a-z]+)', r' \1', str(target_class.__class__.__name__)).split())

@register.simple_tag
def get_verbose_field(instance, field_name):
    """
    Returns verbose_name for a field, starting from an instance.
    """
    return instance._meta.get_field(field_name).verbose_name.title()

@register.simple_tag
def get_help_text(instance, field_name):
    """
    Returns help_text for a field, starting from an instance.
    """
    return instance._meta.get_field(field_name).help_text

@register.simple_tag
def get_verbose_field_from_model_name(app_name, model_name, field_name):
    """
    Returns verbose_name for a field, starting from the model name.
    """
    tmp_model = apps.get_model(app_name, model_name)
    
    return tmp_model._meta.get_field(field_name)._verbose_name.title()

@register.simple_tag
def get_checked_state(field_value):
    """
    Returns the checked property for the checkbox input.
    """
    if(field_value):
        return 'checked=""'
    else:
        return ''

@escape_args
@register.simple_tag
def not_null_str(field_value):
    """
    Returns the not null value for text.
    """
    if(field_value):
        return field_value
    else:
        return ''

@register.simple_tag
def not_null_int(field_value):
    """
    Returns the not null value for integer.
    """
    if(field_value):
        return field_value
    else:
        return 0

@register.simple_tag
def get_combo(app_name, model_name, model_object_id, field_name, op, filter_key = '', filter_value = '', insert_empty_row = True):
    tmp_model = apps.get_model(app_name, model_name)
    if(filter_key):
        # Compongo il dizionario chiave valore da passare al filtro ...
        parsed_filter = {filter_key: filter_value}
        # ... espando il dizionario, in modo da passare i valori al filtro
        tmp_model_objects = tmp_model.objects.filter(**parsed_filter)
    else:
        tmp_model_objects = tmp_model.objects.all()
    
    choice_list = [f"""<option value="{tmp_model_object.id}" selected="" >{tmp_model_object}</option>""" if tmp_model_object.id == model_object_id else f"""<option value="{tmp_model_object.id}" >{tmp_model_object}</option>""" for tmp_model_object in tmp_model_objects]
    if(insert_empty_row):
        choice_list.insert(0, f"""<option value="" selected="" >(nessuno)</option>""" if not model_object_id else f"""<option value="" >(nessuno)</option>""")
    choice_list.insert(0, f"""<select name="{field_name}" class="form-control" id="id_{field_name}" disabled="" >""" if op == 'preview' else f"""<select name="{field_name}" class="form-control" id="id_{field_name}" >""")
    choice_list.append("</select>")
    
    return format_html(mark_safe("\n".join(choice_list)))

@register.simple_tag
def filter_trashed(data_set, show_trashed):
    """
    Filter the given dataset to show trashed or not, based on the 'show_trashed' flag.
    """
    
    if(isinstance(show_trashed, str)):
        show_trashed = (show_trashed == 'True')
        
    if(show_trashed):
        return data_set.all()
    else:
        try:
            return data_set.filter(trash_state = 0)
        except FieldError:
            return data_set.all()
        except AttributeError:
            return data_set.all()
    


    
@register.simple_tag
def format_binary(value):
    return "{0:b}".format(value)

@register.simple_tag
def form_buttons(read_only, submit_action = '', Reset_button = True, Return_button = False, return_url = '', esc_button = False ):
    if(not read_only):
        tmp_html = f'''
                    <div class="panel-footer">
                        <button type="{'button' if submit_action else 'submit'}" class="btn btn-default col-lg-4" {'onClick="' if submit_action else ''}{submit_action}{'"' if submit_action else ''}><img src="{static('img/buttons/Gnome-media-floppy-64.png')}" alt="Conferma" /> Salva</button>
                        <button type="reset" class="btn btn-default col-lg-4"><img src="{static('img/buttons/Gnome-edit-undo-64.png')}" alt="Reset"/> Ripristina</button>'''
        if(esc_button == True): 
            tmp_html +=f'''<button id="Esc"  type="button" class="btn btn-default col-lg-4" onclick="self.close()"><img src="{static('img/buttons/Gnome-esc-64.png')}" alt="Esc"/>Close</button>'''
        tmp_html +=f'''<div class="clearfix"></div>
                    </div> <!-- panel-footer -->'''
    else:
        tmp_html = '''<div class="panel-footer">
                        <p>Solo lettura</p>'''
        if(esc_button == True):            
            tmp_html += f'''<button id="Esc"  type="button" class="btn btn-default col-lg-4" onclick="self.close()"><img src="{static('img/buttons/Gnome-esc-64.png')}" alt="Esc"/>Close</button>'''
        tmp_html += f'''   <div class="clearfix"></div>
                    </div> <!-- panel-footer -->'''

    return format_html(tmp_html)

@register.simple_tag
def form_field_hidden(name, value):
    return f'<input name="{name}" value="{value}" type="hidden">'

@escape_args
@register.simple_tag
def form_field_text(instance, field_name, allow_field_edit, op, field_error = False, indirect_instance = None, indirect_field_name = ''):
    has_error   = ''
    disabled    = ''
    bak_name    = ''
    
        
    if(field_error):
        has_error = 'has-error'
        
    # if(not allow_field_edit and (op in ('edit', 'new_revision', 'preview'))):
    if(not allow_field_edit or op == 'preview'):
        disabled = 'disabled=""'
    
    if(field_name == 'name' and not indirect_instance):
        bak_name = f'<input name="name_bak" value="{getattr( instance, field_name )}" type="hidden">'
    
    if(indirect_instance and indirect_field_name):
        tmp_label = get_verbose_field(indirect_instance, indirect_field_name)
        tmp_help = get_help_text(indirect_instance, indirect_field_name)
    else:
        tmp_label = get_verbose_field(instance, field_name)
        tmp_help = get_help_text(instance, field_name)

    field_value = getattr( instance, field_name ) 

    if(field_value):
        if "}" in field_value or "}" in field_value:
            return (f"""{bak_name}
                        <div class="form-group {has_error}">
                            <label for="id_{field_name}">{tmp_label}</label>
                            <input name="{field_name}" value="{str(field_value)}" class="form-control" id="id_{field_name}" type="text" {disabled}>
                            <p class="help-block">{tmp_help}</p>
                        </div>""")
            
    return format_html(f"""{bak_name}
                        <div class="form-group {has_error}">
                            <label for="id_{field_name}">{tmp_label}</label>
                            <input name="{field_name}" value="{str(field_value)}" class="form-control" id="id_{field_name}" type="text" {disabled}>
                            <p class="help-block">{tmp_help}</p>
                        </div>""")

@register.simple_tag
def form_field_numeric(instance, field_name, op, step = "1"):
    has_error = ''
    disabled = ''
    bak_name = ''
    
    if(op == 'preview'):
        disabled = 'disabled=""'
    
    return format_html(f"""{bak_name}
                <div class="form-group {has_error}">
                    <label for="id_{field_name}">{get_verbose_field(instance, field_name)}</label>
                    <input name="{field_name}" value="{getattr( instance, field_name )}" class="form-control" id="id_{field_name}" type="number" step="{step}" {disabled}>
                    <p class="help-block">{get_help_text(instance, field_name)}</p>
                </div>""")

@escape_args
@register.simple_tag
def form_field_textarea(instance, field_name, op, cols = 40, rows = 5):
    disabled = ""
    
    if(op == 'preview'):
        disabled = 'disabled=""'
        
    return format_html(f"""<div class="form-group">
                            <label for="id_{field_name}">{get_verbose_field(instance, field_name)}</label>
                            <textarea name="{field_name}" cols="{cols}" rows="{rows}" class="form-control" id="id_{field_name}" {disabled}>{not_null_str(getattr( instance, field_name ))}</textarea>
                            <p class="help-block">{get_help_text(instance, field_name)}</p>
                        </div>""")

@register.simple_tag
def form_field_combo(instance, field_name, op, app, model_name, currente_value, filter_key = '', filter_value = '', insert_empty_row = True):
    return format_html(f"""<div class="form-group">
                            <label for="id_{field_name}">{get_verbose_field(instance, field_name)}</label>
                            {get_combo(app, model_name, currente_value, field_name, op, filter_key, filter_value, insert_empty_row)}
                            <p class="help-block">{get_help_text(instance, field_name)}</p>
                        </div>""")

@escape_args    
@register.simple_tag  
def form_field_checkbox(instance, field_name, op, value = True, second_field_name = ''):
    html_tmp =  f"""
                    <div class="form-group">"""
    if second_field_name:            
                    html_tmp +="""<div class="col-lg-4">"""
                    
    html_tmp += f"""<label for="id_{field_name}">{get_verbose_field(instance, field_name)}    </label>
                        <input type="checkbox" class="form-control" name="{field_name}" value="True" {get_checked_state(getattr( instance, field_name ))}/>
                    </div>"""
    if second_field_name:
        html_tmp += f"""<div class="col-lg-4">
                            <label for="id_{field_name}">{get_verbose_field(instance, second_field_name)}</label> 
                            <input type="checkbox" class="form-control" value="True"  name="{second_field_name}" {get_checked_state(getattr( instance, second_field_name ))}/>
                        </div>
                    </div>
                </div>"""
                         
    
    
    return format_html(html_tmp) 
    
def get_csrf_field(request):
    return f"""<input type="hidden" name="csrfmiddlewaretoken" value="{csrf.get_token(request)}">"""

@escape_args
# @print_result
@register.simple_tag
def form_generator(title, name, field_list, csrf_token, url, on_submit = None, close_op = True):
    on_submit_event = f'onsubmit="{on_submit}"' if on_submit else ''
    
    if(close_op):
        close_button = """<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>"""
    else:
        close_button = ""
        
    return format_html(f"""
            <form id='form_edit' action="{url}" method='POST' {on_submit_event} >
                {csrf_token}
                <div class="modal-header">
                            {close_button}
                            <h4 class="modal-title" id="super-standard-form">{title} - ({name if name else ""})</h4>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-lg-12">
                            {field_list}
                        </div>
                    </div>
                </div>
                <div class="modal-body"  id="name_error" hidden>
                    <div class="alert alert-danger">Nome duplicato!</div>
                </div>
                <div class="modal-footer">
                    <button type="submit" class="btn btn-primary">Salva</button>
                    <button type="reset"  class="btn btn-primary">Resetta</button>
                    <button type="button" class="btn btn-default" data-dismiss="modal">Annulla</button>
                </div>
            </form>
        """)
    
@escape_args
@register.simple_tag    
def table_generator(title, columns, row_html, close_op = True):
    
    if(close_op):
        close_button = """<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>"""
    else:
        close_button = ""
    
    return f"""
            <div class="panel-heading">
                {close_button}
                <h4 class="modal-titl" id="myModalLabel"> </h4>
            </div>
            <div class="panel-body">
                <table  style="width: 100%" class="display table table-striped table-bordered table-hover" id="">
                    <thead>
                        <tr>
                            {columns_html(columns)}
                        </tr>
                    </thead>
                    <tbody id="tbody">
                        {row_html}
                    </tbody>
                </table>
            </div>
        
        <script>
        
            $(document).ready(function() {{
                $('table.display').DataTable({{
                    lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "All"]],
                    responsive: true,
                    autoWidth: false,
                    destroy: true,
                }});
                ChangeCurrentCell();
            }});
            
            function sleep (time) {{
              return new Promise((resolve) => setTimeout(resolve, time));
            }};
            
            sleep(600).then(() => {{
                $('div.dataTables_filter input').focus();
                $("div.dataTables_length select")[0].autofocus=false;
                $('#dataTables-example_length select')[0].onchange = function() {{
                    $('div.dataTables_filter input').focus();
                }}
                $('#dataTables-example_length select')[0].onmousedown = function() {{
                    $('div.dataTables_filter input').focus();
                }}
            }});
                   
            
        </script>"""

@escape_args
@register.simple_tag
def table_button_generator(op_type, on_click, grafic_icon = True, element_id = 0, disable = False):
    
    class_attribute = 'btn btn-outline btn-default btn-xs'
    src_attribute = ''
    img_id_attribute = ''
    html_img = ''
    title_attribute = ''
    diseble_html = ''
    
    if(op_type == sh.OP_NEW):
        if(grafic_icon):
            title_attribute = 'Nuovo'
            src_attribute = 'img/buttons/Gnome-document-new-24.png' 
        else:
            title_attribute = 'Nuovo'
            class_attribute = 'btn btn-default btn-xs glyphicon-plus'
            
    if(op_type == sh.OP_EDIT):
        title_attribute = 'Modifica'
        src_attribute = 'img/buttons/Gnome-accessories-text-editor-24.png'
    
    if(op_type == sh.OP_HISTORY):
        title_attribute = 'Mostra Storico'
        src_attribute = 'img/buttons/Gnome-document-open-last-24.png'
        
    if(op_type == sh.OP_PREVIEW):
        title_attribute = 'Anteprima'
        src_attribute = 'img/buttons/Gnome-lens-24.png'
    
    if(op_type == sh.OP_DUPLICATE):
        title_attribute = 'Duplica'
        src_attribute = 'img/buttons/Gnome-edit-copy-24.png'
    
    if(op_type == sh.OP_TRESH):
        title_attribute = 'Elimina'
        src_attribute = 'img/buttons/Gnome-edit-delete-24.png'
    
    if(op_type == sh.OP_RESTORE):
        title_attribute = 'Ripristina'
        src_attribute = 'img/buttons/Gnome-edit-undo-24.png'
    
    if(op_type == sh.OP_DELETE):
        title_attribute = 'Elimina definitivamente'
        src_attribute = 'img/buttons/Gnome-delete-24.png'
    
    if(op_type == sh.OP_MOVE):
        title_attribute = 'Sposta'
        src_attribute = 'img/buttons/Gnome-move-24.png'
    
    if(op_type == sh.OP_MOVE_UP):
        title_attribute = 'Muovi Su'
        src_attribute = 'img/buttons/Gnome-move-up-24.png'
    
    if(op_type == sh.OP_MOVE_DOWN):
        title_attribute = 'Muovi Giù'
        src_attribute = 'img/buttons/Gnome-move-down-24.png'
    
    if(op_type == sh.OP_PUBLISH):
        title_attribute = 'Pubblica'
        src_attribute = 'img/buttons/Gnome-publish-24.png'
    
    if(op_type == sh.OP_NEW_REVISION):
        title_attribute = 'Nuova Revisione'
        src_attribute = 'img/buttons/Gnome-new-revisio-24.png'
    
    if(op_type == sh.OP_ADD):
        title_attribute = 'Aggiungi'
        src_attribute = 'img/buttons/Gnome-list-add-24.png'
    
    if(op_type == sh.OP_REMOVE):
        title_attribute = 'Rimuovi'
        src_attribute = 'img/buttons/Gnome-list-remove-24.png'
        
    if(op_type == sh.OP_UPDATE):
        title_attribute = 'Update'
        src_attribute = 'img/buttons/Gnome-update-32.png'
        
    if(op_type == sh.OP_GOTO):
        title_attribute = 'Goto'
        src_attribute = 'img/buttons/Gnome-goto-24.png'
        
    if(src_attribute):
        if(element_id):
            img_id_attribute = f"""id="img_{element_id}" """
            
        html_img = f"""<img src="{static(src_attribute)}" alt="{title_attribute}" {img_id_attribute}>"""
        
    if(disable):
        diseble_html = "disabled = 'disabled'"
    html_button = f"""<button type="button" class="{class_attribute}" onclick="{on_click}" title="{title_attribute}" {diseble_html}>{html_img}</button>"""
    
    return html_button
                
def columns_html(columns):
    tmp_html="".join(f"<th style='widht:300px'>{column}</th>"  if column else f"<th style='widht:0px'>{column}</th>"for column in columns)
    return tmp_html



    

@register.simple_tag
def get_table_simple_row(main_object_list, father_id_name, worker_id, header_url, op = 'edit', show_trashed = False, show_history = False, father_col = False):
    
    html_tmp = ""
    image_warning = '<img src="%s" title="Target Non Compilato" alt="!!!"/>' % static('img/buttons/Gnome-dialog-warning-24.png')
    attribute_list = [f"""
                        <tr id="{'target_' if hasattr(main_object,'attribute') else 'attribute_'}{main_object.id}" >
                            <td>{table_button_generator(sh.OP_EDIT , sh.create_href_url(reverse(header_url, args = [main_object.id, getattr(main_object, father_id_name), worker_id, sh.OP_EDIT, show_trashed, show_history]))) if op=='edit' else table_button_generator(sh.OP_PREVIEW , sh.create_href_url(reverse(header_url, args = [main_object.id, getattr(main_object, father_id_name), worker_id, sh.OP_PREVIEW, show_trashed, show_history])))}</td>
                            <td>{ image_warning if hasattr(main_object,'attribute') and main_object.attribute == None else '' }{main_object.name}</td>
                            <td>{main_object.description}</td>
                            <td>{main_object._getTypeChild()}</td>
                            <td>{table_button_generator(sh.OP_TRESH if main_object.trash_state == 0 else sh.OP_RESTORE,sh.js_base_function_generetor("change_trash_property", (('target_' if hasattr(main_object,'attribute') else 'attribute_') + str(main_object.id)), reverse(header_url, args = [main_object.id, getattr(main_object, father_id_name), worker_id, sh.OP_TRESH, show_trashed, show_history])), element_id = (('target_' if hasattr(main_object,'attribute') else 'attribute_') + str(main_object.id))) if not main_object.obbligatory else "" }</td>
                        </tr>
                    """ 
                            for main_object in main_object_list]
    
    html_rows = "".join(["".join(attribute) for attribute in attribute_list])
    html_tmp = f"{html_tmp} {html_rows}"
        
    return  html_tmp 

@register.simple_tag
def get_table_complete_row(main_object_list, father_id_name, worker_id, header_url, op = 'edit', show_trashed = False, show_history = False, father_col = False):

    html_tmp = ""

    attribute_list = [f"""
                        <tr id="{'target_' if hasattr(main_object,'attribute') else 'attribute_'}{main_object.id}">
                            <td>{table_button_generator(sh.OP_EDIT , sh.create_href_url(reverse(header_url, args = [main_object.id, getattr(main_object, father_id_name), worker_id, sh.OP_EDIT, show_trashed, show_history]))) if op=='edit' else table_button_generator(sh.OP_PREVIEW , sh.create_href_url(reverse(header_url, args = [main_object.id, getattr(main_object, father_id_name), worker_id, sh.OP_PREVIEW, show_trashed, show_history])))}</td>
                            <td>{main_object.name}</td><td>{main_object.description}</td><td>{main_object._getTypeChild()}</td>
                            <td>{main_object._getFatherName()}</td>
                            <td>{table_button_generator(sh.OP_TRESH if main_object.trash_state == 0 else sh.OP_RESTORE,sh.js_base_function_generetor("change_trash_property", (('target_' if hasattr(main_object,'attribute') else 'attribute_') + str(main_object.id)), reverse(header_url, args = [main_object.id, getattr(main_object, father_id_name), worker_id, sh.OP_TRESH, show_trashed, show_history])), element_id = (('target_' if hasattr(main_object,'attribute') else 'attribute_') + str(main_object.id))) if not main_object.obbligatory else "" }</td>
                        </tr>
                    """ 
                            for main_object in main_object_list]
    
    html_rows = "".join(["".join(attribute) for attribute in attribute_list])
    html_tmp = f"{html_tmp} {html_rows}"
        
    return  html_tmp 


def button_generator_function(element_name, id_element, type_element, onClick):
    html_button = ""

    #if (hasattr(model_object_tag, 'brick')):
        #action = f"{reverse('brick_tag_struttura', args = [model_object_tag.id if model_object_tag.id else 0, model_object_tag.brick.id, 'edit' ])}"
    
    #elif (hasattr(model_object_tag, 'state_run')):
        #action = f"{reverse('tag_link_element_struttura', args = [model_object_tag.id if model_object_tag.id else 0, model_object_tag.state_run.id, 'edit' ])}"
    
    #elif (hasattr(model_object_tag, 'recipe_config_page')):
        #action = f"{reverse('recipe_config_element_struttura', args = [model_object_tag.id if model_object_tag.id else 0, model_object_tag.recipe_config_page.id, 'change_tag' ])}"
    
    #elif (hasattr(model_object_tag, 'tag_elements')):
        #action = f"{reverse('monitor_config_element_struttura', args = [model_object_tag.id if model_object_tag.id else 0, id_element, 'add' ])}"
    

    #elif(hasattr(model_object_tag, 'tags')):  
    if(type_element):
        html_button = f"""<button id = "{element_name}_{id_element}" type="button" class="btn btn-success btn-xs" data-toggle="tooltip" value= "{type_element}" data-placement="bottom" onClick="{onClick}" >{type_element}</button>""" 
    else:
        html_button = f"""<button id = "{element_name}_{id_element}" type="button" class="btn btn-danger btn-xs" data-toggle="tooltip" value= "{type_element}" data-placement="bottom" onClick="{onClick}" >{type_element}</button>""" 

    return html_button

        
@register.simple_tag 
def generate_state_row(model_object, type_obj, op, request, flag_set_goto = False ):
    state=model_object.get_origin
    state_chart=state.state_chart
    state_list=[]
    if(type_obj=='action_group'):
        state_list.append([f"""<tr><td>{button_generator_function_state(model_object, state, type_obj, 'state', op, request)}</td><td>{state.name}</td><td>state</td></tr>""" for state in state_chart.states.filter(trash_state=0) if len(state.state_action_groups.all())==0])
        state_list.append([f"""<tr><td>{button_generator_function_state(model_object, state, type_obj, 'safety', op, request)}</td><td>{state.name}</td><td>safety</td></tr>""" for state in state_chart.safeties.filter(trash_state=0) if len(state.safety_action_groups.all())==0])
    else:
        if(flag_set_goto):
            action = f"{reverse('condition_group_struttura',      args = [model_object.id if model_object.id else 0, 0, op, model_object.get_type])}"
            state_list.append([f"""<tr><td><button id="button_state_null" type="button" class="btn btn-default btn-xs" onClick="button_state_function({model_object.id}, 0, '{action}', '{type_obj}');"><img src="{static('img/buttons/Gnome-go-next-24.png')}" alt="Seleziona"/></button> </td><td> -nessun goto- </td><td>state</td></tr>"""])
        state_list.append([f"""<tr><td>{button_generator_function_state(model_object, state, type_obj, 'state', op, request)}</td><td>{state.name}</td><td>state</td></tr>""" for state in state_chart.states.filter(trash_state=0)])
        if(not flag_set_goto):
            state_list.append([f"""<tr><td>{button_generator_function_state(model_object, state, type_obj, 'safety', op, request)}</td><td>{state.name}</td><td>safety</td></tr>""" for state in state_chart.safeties.filter(trash_state=0)])
    html_rows = "".join(["".join(element) for element in state_list])
    return html_rows

@register.simple_tag 
def get_debug_row(list_element, request):
    row_list = []
    row_list.append([f"""<tr><td><button id="button_debug" type="button" class="btn btn-default btn-xs" onClick="debug_goto({element['cordinate']})"><img src="{static('img/buttons/Gnome-go-next-24.png')}" alt="Seleziona"/></button></td><td>{element['description']}</td></tr>""" for element in list_element])
    html_rows = "".join(["".join(element) for element in row_list])
    return html_rows


def button_generator_function_state(model_object, state, type_obj, origin, op, request):
        if(type_obj=='action_group'):
            action = f"{reverse('action_group_struttura',      args = [model_object.id if model_object.id else 0, state.id, op, origin])}"
        else:
            action = f"{reverse('condition_group_struttura',      args = [model_object.id if model_object.id else 0, state.id, op, origin])}"
        return f"""<button id="button_state_{state.id}" type="button" class="btn btn-default btn-xs" onClick="button_state_function({model_object.id}, {state.id}, '{action}', '{type_obj}');"><img src="{static('img/buttons/Gnome-go-next-24.png')}" alt="Seleziona"/></button>""" 

@register.simple_tag
def button_trash_generator(model_object, row_id_prefix, url, show_trashed, op, enable_edit = True):
    try:
        if(model_object.trash_state):
            html_img = f"""<img id="img_{model_object.id}" src="{static('img/buttons/Gnome-edit-undo-24.png')}" alt="Ripristina" />"""
        else:
            html_img = f"""<img id="img_{model_object.id}" src="{static('img/buttons/Gnome-edit-delete-24.png')}" alt="Elimina" />"""
            
    except AttributeError:
        html_img = f"""<img id="img_{model_object.id}" src="{static('img/buttons/Gnome-edit-delete-24.png')}" alt="Elimina" />"""    
        
    if(enable_edit and not op == "preview"):
        html_onclick = f"""change_tresh_field('{url}', 'img_{model_object.id}', '{row_id_prefix}_{model_object.id}', '{show_trashed}')"""
        html_disabled = f""""""
    else:
        html_onclick = f"""alert("Modifiche non abilitate")"""
        html_disabled = f"""disabled="" """
    
    html_button = f"""<button type="button" class="btn btn-outline btn-default btn-xs" onClick="{html_onclick}" {html_disabled}>{html_img}</button>"""
    
    return format_html(html_button)
    
@register.simple_tag(takes_context = True)
def get_import_export_panel(context, url, file_type, file_description, op = 'edit'):
    if op == 'preview':
        hidden_buttun   = 'style="display:none;"'
        hidden          = 'hidden'
        title           = 'Esporta'
        read_only_label = f"""
                            <div class="col-lg-3">
                                <label for="id_file_to_import">Modalità solo lettura!!!</label>
                            </div>
                        """
    else:
        hidden_buttun   = ''
        hidden          = ''
        title           = 'Importazione Ed Esportazione'
        read_only_label = ''
        
    return format_html(f"""
        <div class="panel panel-default" id="import_export_panel">
            <div class="panel-heading" >
                {title}
            </div>  <!-- /.panel-heading -->
            
            <form action="{url}" method="POST" enctype="multipart/form-data">
                <input type="hidden" name="csrfmiddlewaretoken" value="{context.get('csrf_token', '')}" >
                <div class="panel-body" {hidden}>
                   <div class="row">
                       <div class="col-lg-6" {hidden}>
                            <div class="form-group">
                                <label for="id_file_to_import">File {file_type}</label>
                                <input name="file_to_import" class="form-control" id="id_file_to_import" type="file">
                                <p class="help-block">Il formato del file da caricare deve essere questo:</p>
                                <p class="help-block">{file_description}</p>
                            </div>
                        </div> <!-- col-lg-6-->
                            
                       <div class="col-lg-6">
                            <div class="form-group" {hidden}>
                                <label for="id_description">Tipo Importazione</label>
                                <p><input type="radio" name="import_mode" value="reset"> Resetta lista<br></p>
                                <p><input type="radio" name="import_mode" value="append" checked> Accoda alla lista attuale<br></p>
                                <p class="help-block">Indicare come si vuole effettuare l'importazione</p>
                            </div>
                       
                        </div> <!-- col-lg-6-->
    
                    </div>
                </div> <!-- /.panel-body -->
                
                <div class="panel-footer">
                    <button type="submit" class="btn btn-default col-lg-3" {hidden_buttun}><img src="{static('img/buttons/Gnome-go-up-64.png')}" alt="Conferma"/> Importa</button>
                    <button type="button" class="btn btn-default col-lg-3" onClick="export_function();" ><img src="{static('img/buttons/Gnome-go-down-64.png')}" alt="Conferma"/> Esporta</button>
                    {read_only_label}
                    <div class="clearfix"></div>
                </div> <!-- panel-footer -->
    
            
            </form>
        </div> <!-- /.panel -->
        
    """)

@register.simple_tag
def table_wait_animation(flatten_string = False):
    """Crea una sezione con l'animazione del carimaento in corso."""
    html_animation = f"""
        <div class="panel panel-default">
            <img src="{static("img/animations/blob_loading.gif")}" alt="Caricamento in corso ..." title="Caricamento in corso ..."/>
            <h3>Caricamento in corso ...</h3>
        </div>"""
    
    if(flatten_string):
        html_animation = html_animation.replace('\n', '').replace('\r', '')
        
    return format_html(html_animation)

