from django.db import models
from base.models import FaskObject, EditInfo, StandardForm
from django.contrib.auth.models import User

class ProjectState(FaskObject):
    """
    This is the state of the Project.
    """
    pass

class Project(FaskObject, EditInfo):
    """
    This is the Project model, and it contain some simple info and the list
    of task to execute.
    """
    start_date = models.DateField(verbose_name = "Start Date", help_text = "When project should start", blank = True, null = True)
    end_date = models.DateField(verbose_name = "End Date", help_text = "When project should end", blank = True, null = True)
    state = models.ForeignKey(ProjectState, verbose_name = "State", help_text = "The progression state of the project", related_name = 'project_state', to_field = 'id', blank = True, null = True)
    supervisor = models.ForeignKey(User, verbose_name = "Supervisor", help_text = "Who is the project supervisor", related_name = 'project_supervisor', blank = True, null = True)

    

""" ***************************************************************************

                                    ModelForms

    *************************************************************************** """

class ProjectForm(StandardForm):
    class Meta:
        model = Project
        fields = '__all__'