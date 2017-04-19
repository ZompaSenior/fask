from django.db import models

from base.models import FaskObject, EditInfo
from task.models import Task

class SubTask(FaskObject, EditInfo):
    """
    This is the task, with all its management information.
    """
    task = models.ForeignKey(Task, verbose_name = "Task", help_text = "The owner task", related_name = 'task_owner')
    completed_on = models.DateField(verbose_name = "Completed Date", help_text = "When sub task was completed")
