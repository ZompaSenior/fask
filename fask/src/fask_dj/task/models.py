from django.db import models
from base.models import FaskObject, EditInfo, StandardForm
from django.contrib.auth.models import User
from project.models import Project

class TaskPriority(FaskObject):
    """
    Indicate a priority on between the task.
    """
    pass

class TaskProgression(FaskObject):
    """
    Indicate a priority on between the task.
    """
    pass

class Task(FaskObject, EditInfo):
    """
    This is the task, with all its management information.
    """
    project = models.ForeignKey(Project, verbose_name = "Project", help_text = "The project that is the task owner", related_name = 'task_project_owner', blank = True, null = True)
    due_to = models.DateField(verbose_name = "Due To", help_text = "When task has to be completed", blank = True, null = True)
    completed_on = models.DateField(verbose_name = "End Date", help_text = "When task was completed", blank = True, null = True)
    assigned_to = models.ForeignKey(User, verbose_name = "Assigned To", help_text = "Who is executing the task", related_name = 'task_assignee', blank = True, null = True)
    priority = models.ForeignKey(TaskPriority, verbose_name = "Priority", help_text = "How the task is urgent", related_name = 'task_priority', blank = True, null = True)
    progression = models.ForeignKey(TaskProgression, verbose_name = "Proression", help_text = "What is the progression state of the task", related_name = 'task_progression', blank = True, null = True)

    
    

""" ***************************************************************************

                                    ModelForms

    *************************************************************************** """

class TaskForm(StandardForm):
    class Meta:
        model = Task
        fields = '__all__'
    
    def set_project(self, project_id):
        self.fields.project = Project.objects.get(pk = project_id)