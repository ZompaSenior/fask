from django.db import models
from fask_dj.base.models import FaskObject, EditInfo
from django.contrib.auth.models import User

class Project(FaskObject, EditInfo):
    """
    This is a base metaclass for have a common structure in any standard
    object of the application.
    It is defined as 'abstract' so where inherited in othe class create
    all the field in the sons class tables.
    """
    start_date = models.DateField(verbose_name = "Start Date", help_text = "When project should start")
    end_date = models.DateField(verbose_name = "End Date", help_text = "When project should end")
    supervisor = models.ForeignKey(User)
    
