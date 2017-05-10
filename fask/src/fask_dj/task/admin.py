from django.contrib import admin

from .models import TaskPriority, TaskProgression

admin.site.register(TaskPriority)
admin.site.register(TaskProgression)