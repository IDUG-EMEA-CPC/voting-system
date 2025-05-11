from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect, render
from ..views.views_login import login

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import template

#from django.shortcuts import redirect, render
#from ..authentication.views import login_view as login



def index(request):
    if request.user.is_authenticated:
        template = loader.get_template('home/index.html')
        context = {'segment': 'index'}
        return HttpResponse(template.render(context, request))
    else:
        return redirect(login)


def encode_values(request):
    if request.user.is_authenticated:
        template = loader.get_template('home/encode_values.html')
        context = {'segment': 'encode'}
        return HttpResponse(template.render(context, request))
    else:
        return redirect(login)


def form_sample(request):
    if request.user.is_authenticated:
        template = loader.get_template('home/form_elements.html')
        context = {'segment': 'form'}
        return HttpResponse(template.render(context, request))
    else:
        return redirect(login)


def moderator(request):
    if request.user.is_authenticated:
        template = loader.get_template('home/moderator.html')
        context = {'segment': 'moderator'}
        return HttpResponse(template.render(context, request))
    else:
        return redirect(login)