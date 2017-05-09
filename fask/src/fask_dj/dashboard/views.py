from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

def dashboard(request):
    template = loader.get_template('dashboard.html')
    context = {}
    return HttpResponse(template.render(context, request))