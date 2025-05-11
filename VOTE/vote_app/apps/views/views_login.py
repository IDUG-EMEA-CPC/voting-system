
from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout, login as django_login
from django.template import RequestContext
from django.template import loader
from ..score.utils import init_response_context
from django.http import HttpResponse

from django.contrib.auth import authenticate
from ..score.forms import LoginForm


def login(request):
    if request.user.is_authenticated:
        print('already auth')
        return redirect('index.html')
    else:
        form = LoginForm(request.POST or None)

        msg = None

        if request.method == "POST":

            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")

                request.session['building_process'] = request.POST.get('building_process', '')

                user = authenticate(username=username, password=password)
                if user is not None:
                    django_login(request, user)
                    return redirect("/")
                else:
                    msg = 'Invalid credentials'
            else:
                msg = 'Error validating the form'

        return render(request, "accounts/login.html", {"form": form, "msg": msg})



def logout(request):
    print('LOGOUT')
    request_context = RequestContext(request)
    print(request_context)

    django_logout(request)
    return redirect(login)

