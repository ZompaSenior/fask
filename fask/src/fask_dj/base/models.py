from django.db import models

class FaskObject(models.Model):
    """
    This is a base metaclass for have a common structure in any standard
    object of the application.
    It is defined as 'abstract' so where inherited in othe class create
    all the field in the sons class tables.
    """
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length = 200, verbose_name = "Description", help_text = "The short description for that element")
    annotation = models.TextField(verbose_name = "Annotation", help_text = "Here you can give more deep information")
    
    class Meta():
        abstract = True

class EditInfo(models.Model):
    """
    This is a base metaclass for all editable object of the application.
    It is defined as 'abstract' so where inherited in othe class create
    all the field in the sons class tables.
    """
    creation_date = models.DateField(auto_now_add = True, verbose_name = "Creation Date", help_text = "When the element was created")
    edit_date = models.DateField(auto_now = True, verbose_name = "Edit Date", help_text = "When the element was modified last time")
    creation_user = models.TextField(verbose_name = "Creation User", help_text = "Who created the element")
    edit_user = models.TextField(verbose_name = "Edit User", help_text = "Who modified the element last time")
    
    class Meta():
        abstract = True

