from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect, render
from ..views.views_login import login

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import template

import math

#from django.shortcuts import redirect, render
#from ..authentication.views import login_view as login

from ..score.utils import RequestParameters, retrieve_value_from_session, init_response_context
from .views_add import refresh_values

from ..score.models import Sessioneval, Session, Best_Session, Tracks
from ..tables.tables import SessionEvalTable
from django_tables2 import RequestConfig

from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models.functions import Substr


def index(request):
    if request.user.is_authenticated:
        context = init_response_context(request)
        context['segment'] = 'index'

        check = Sessioneval.objects.all().count()
        if check > 0:

            # encoded sessions
            encode_sessions = Sessioneval.objects.all().values("sessioncode").annotate(total=Count("sessioncode")).count()
            sessions_nb = Session.objects.all().count()
            session_percent = round((encode_sessions/sessions_nb)*100 , 2)

            context['encode_sessions'] = encode_sessions
            context['sessions_nb'] = sessions_nb
            context['session_percent'] = session_percent

            # best session
            best_session = Best_Session.objects.all()

            context['best_sessioncode'] = best_session[0].sessioncode
            context['best_speaker'] = best_session[0].primarypresenterfullname
            context['best_rating'] = round(best_session[0].rating, 4)

            #track summary
            track_summary = Session.objects.annotate(first=Substr('sessioncode', 1, 1)).values('first').annotate(cnt=Count('sessioncode')).order_by('first')
            nb_per_session = Sessioneval.objects.annotate(session=Substr('sessioncode', 1, 3)).values('session').annotate(cnt=Count('sessioncode')).order_by('session')

            i = 0
            for track in track_summary:
                track_summary[i]['nb'] = 0
                track_summary[i]['percent'] = 0
                count = 0
                for nb in nb_per_session:
                    if nb['session'][:1] == track['first']:
                        count += 1
                        track_summary[i]['nb'] = count
                        track_summary[i]['percent'] = round((count/track['cnt'])*100 , 2)
                        # track detail
                        detail = Tracks.objects.annotate(first=Substr('sessioncode', 1, 1)).filter(first=track['first']).values().order_by('first', 'sessioncode')
                        track_summary[i]['detail'] = detail

                i += 1

            context['tracks'] = track_summary


        else:
            # encoded sessions
            context['encode_sessions'] = 0
            context['sessions_nb'] = Session.objects.all().count()
            context['session_percent'] = 0

            # best session
            context['best_sessioncode'] = "None"
            context['best_speaker'] = ""
            context['best_rating'] = 0


        template = loader.get_template('home/index.html')

        return HttpResponse(template.render(context, request))
    else:
        return redirect(login)


def encode_values(request):
    if request.user.is_authenticated:
        if request.GET:

            sessioncode = request.session['session_code']

            template = loader.get_template('home/encode_values.html')
            context = {'segment': 'encode', 'session_code': sessioncode}
            return HttpResponse(template.render(context, request))

        else:
            template = loader.get_template('home/encode_values.html')
            context = {'segment': 'encode'}
            return HttpResponse(template.render(context, request))
    else:
        return redirect(login)



def sessions(request):
    if request.user.is_authenticated:
        template = loader.get_template('home/sessions.html')
        context = {'segment': 'sessions'}
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