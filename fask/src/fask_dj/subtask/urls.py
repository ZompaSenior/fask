"""fask_dj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from subtask import views

urlpatterns = [
    url(r'^subtasks', views.subtasks, name = 'subtasks'),
    url(r'^subtask/(?P<subtask_id>[0-9]+)/$', views.subtask, name = 'subtask'),
    url(r'^subtask_delete/(?P<subtask_id>[0-9]+)/$', views.subtask_delete, name = 'subtask_delete'),
    url(r'^subtask_task/(?P<subtask_id>[0-9]+)/(?P<task_id>[0-9]+)/(?P<redirect_name>[a-z]+)$', views.subtask_task, name = 'subtask_task'),
]
