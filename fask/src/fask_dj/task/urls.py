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

from . import views

urlpatterns = [
    url(r'^tasks', views.tasks, name = 'tasks'),
    url(r'^task/(?P<task_id>[0-9]+)/$', views.task, name = 'task'),
    url(r'^task_delete/(?P<task_id>[0-9]+)/$', views.task_delete, name = 'task_delete'),
    url(r'^task_project/(?P<task_id>[0-9]+)/(?P<project_id>[0-9]+)/(?P<redirect_name>[a-z]+)$', views.task_project, name = 'task_project'),
]
