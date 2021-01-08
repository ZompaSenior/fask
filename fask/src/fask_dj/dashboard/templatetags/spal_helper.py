# -*- coding: Cp1252 -*-
"""
Contiene funzioni e variabili di comune utilità per tutto il progetto.
"""
from django.shortcuts import get_object_or_404

__author__ = "ZOMPARELLIL"
__version__ = "0.1.0"
__license__ = "Spal Automotive, 2018"

OP_NEW                  = 'new'
OP_EDIT                 = 'edit'
OP_PREVIEW              = 'preview'
OP_DUPLICATE            = 'duplicate'
OP_TRESH                = 'delete'
OP_RESTORE              = 'restore'
OP_DELETE               = 'delete_permanent'
OP_MOVE                 = 'move'
OP_MOVE_UP              = 'move_up'
OP_MOVE_DOWN            = 'move_down'
OP_PUBLISH              = 'publish'
OP_NEW_REVISION         = 'new_revision'
OP_ADD                  = 'add'
OP_REMOVE               = 'remove'
OP_UPDATE               = 'update'
OP_GOTO                 = 'goto'
OP_HISTORY              = 'show_history'

def from_checkbox_to_booleanfield(post_value: str):
    """Trasforma il 'value' dei campi tipo checkbox in un boolean.
    
    Args:
        post_value (str): il valore POST inviato
    
    Returns:
        bool: lo stato di checked
        
    """
        
    if(post_value):
        if(post_value == 'True' or post_value == 'on' or post_value == 'true'):
            return True
        else:
            return False
    else:
        return False

def from_id_to_model(post_value: str, object_model):
    """Ricava un oggetto dall'id passato a 'value'.
    
    Args:
        post_value (str): il valore POST inviato
        
        object_model (model): il modello di cui cercare l'oggetto
    
    Returns:
        object: l'oggetto di tipo 'object_model'
        
    """
        
    try:
        mdoel_id = int(post_value)
    except:
        mdoel_id = 0
        
    if(mdoel_id):
        return get_object_or_404(object_model, pk = mdoel_id)
    else:
        return None

def create_href_url(object_url):
    return f"location.href='{object_url}'"

def js_confirm_function(text, object_url, confirm_msg = None):
    return f"{text}('{object_url}', '{confirm_msg}')"

def js_caLL_function_generetor(text, object_id, object_url, tr_location = None, show_trashed = None):
    object_url = str(object_url)
    if(object_id):
        object_id = str(object_id)
    if(show_trashed):
        return f"{text}('{object_id}', '{object_url}', '{tr_location}', '{show_trashed}')"
        
    elif((tr_location==None) and (object_id==None)):
        return f"{text}('{object_url}')"
    
    elif((tr_location==None)):
        return f"{text}('{object_id}', '{object_url}')"
    
def js_base_function_generetor(text, object_id, object_url):
    object_url = str(object_url)
    return f"""{text}('{object_id}', 'img_{object_id}', '{object_url}')"""
    
def js_caLL_function_only_url(text, object_url_first, object_url_second = None):
    object_url_first = str(object_url_first)
    if(object_url_second):
        object_url_second = str(object_url_second)
        return f"{text}('{object_url_first}', '{object_url_second}')"
    
    else:
        return f"{text}('{object_url_first}')"