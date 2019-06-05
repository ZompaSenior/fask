from django.db import models
from django.forms import ModelForm
from django.forms.models import ModelChoiceField
from django.contrib.auth.models import User
from django.forms.fields import DateField, DateTimeField


class FaskObject(models.Model):
    """
    This is a base metaclass for have a common structure in any standard
    object of the application.
    It is defined as 'abstract' so where inherited in othe class create
    all the field in the sons class tables.
    """
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length = 200, verbose_name = "Description", help_text = "The short description for that element")
    annotation = models.TextField(verbose_name = "Annotation", help_text = "Here you can give more deep information", blank = True)
    
    class Meta():
        abstract = True
    
    def __str__(self):
        return self.description
        

class EditInfo(models.Model):
    """
    This is a base metaclass for all editable object of the application.
    It is defined as 'abstract' so where inherited in othe class create
    all the field in the sons class tables.
    """
    creation_date = models.DateField(auto_now_add = True, verbose_name = "Creation Date", help_text = "When the element was created")
    edit_date = models.DateField(auto_now = True, verbose_name = "Edit Date", help_text = "When the element was modified last time")
    creation_user = models.CharField(max_length = 200, verbose_name = "Creation User", help_text = "Who created the element", blank = True)
    edit_user = models.CharField(max_length = 200, verbose_name = "Edit User", help_text = "Who modified the element last time", blank = True)
    
    class Meta():
        abstract = True


""" ***************************************************************************

                                    ModelForms

    *************************************************************************** """


class StandardForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(StandardForm, self).__init__(*args, **kwargs)
        for key, field in self.fields.items():
            # Setta la classe per il css per le visualizzazione
            field.widget.attrs.update({'class': 'form-control'})
            # In caso di campo a scelta
            if(type(field) is ModelChoiceField):
                # Setta il testo per nessuna selezione
                field.empty_label = "(nessuno)"
                
                # Imposta l'ordinamento nella combo
                if(field.choices.queryset.model == User):
                    field.queryset = field.queryset.order_by('first_name')
                else:
                    field.queryset = field.queryset.order_by('description')
            
            if(key in ('revision', 'trash_state', 'creation_date', 'edit_date', 'creation_user', 'edit_user')):
                field.widget.attrs['readonly'] = True
           
            if (type(field) is DateField):
                field.widget.input_type ='date'
                
                
                
            


    def set_user(self, user_info):
        self.user_info = user_info
    
    def set_revision(self, revision):
        self.revision = revision

    def clean_create_user(self):
        data = self.cleaned_data['creation_user']
        
        if(self.user_info):
            if(len(data)<=0):
                data = str(self.user_info)
    
        return data
    
    def clean_edit_user(self):
        data = self.cleaned_data['edit_user']
        
        if(self.user_info):
            data = str(self.user_info)
        
        return data

    def clean_revision(self):
        data = self.cleaned_data['revision']
        
        if(self.revision):
            data = str(self.revision)
    
        return data
