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
from task.views import task_project
from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^task_calendar/$', views.task_calendar, name='task_calendar'),
    url(r'^task_calendar_details_request/(?P<select_day>[0-9]+)/(?P<negative>[\w]+)/$', views.task_calendar_details_request, name='task_calendar_details_request'),
    url(r'^task_project/(?P<task_id>[0-9]+)/(?P<project_id>[0-9]+)/(?P<redirect_name>[\w]+)/$', task_project, name='task_project'),
]
