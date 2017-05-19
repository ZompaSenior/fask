from django.db import models

from base.models import FaskObject, EditInfo, StandardForm
from task.models import Task
from django.template.defaultfilters import default

class SubTask(FaskObject, EditInfo):
    """
    This is the subtask, with all its management information.
    """
    task = models.ForeignKey(Task, verbose_name = "Task", help_text = "The owner task", related_name = 'task_owner')
    completed = models.BooleanField(verbose_name = "Completed", help_text = "If sub task was completed", default = False)
    completed_on = models.DateField(verbose_name = "Completed Date", help_text = "When sub task was completed", blank = True, null = True)

    
    

""" ***************************************************************************

                                    ModelForms

    *************************************************************************** """

class SubTaskForm(StandardForm):
    class Meta:
        model = SubTask
        fields = '__all__'
