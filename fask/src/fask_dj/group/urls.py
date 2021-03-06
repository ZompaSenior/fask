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
    url(r'^groups', views.groups, name = 'groups'),
    url(r'^group/(?P<group_id>[0-9]+)/$', views.group, name = 'group'),
    url(r'^group_delete/(?P<group_id>[0-9]+)/$', views.group_delete, name = 'group_delete'),
]# url(r'^$', views.index, name='index'),
