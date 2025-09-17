from django.template import loader
from django.shortcuts import redirect, render
from ..views.views_login import login
from ..score.utils import RequestParameters, retrieve_value_from_session, init_response_context
from ..score.models import Session, Moderators
from django.http import JsonResponse
from rest_framework import status

from django.core.paginator import Paginator
from django.template.loader import render_to_string


def refresh_moderator(request):
    if not request.user.is_authenticated:
        print('out of session')
        content = {
            'message': 'Your session has expired. Please <a href="./login.html">login</a>'
        }
        return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        # retrieving parameters
        x = RequestParameters()  # generic class for request parameters

        for key in ['sessioncode']:
            setattr(x, key, retrieve_value_from_session(request, key))

        context = init_response_context(request)

        session = Session.objects.all().filter(session_code=x.sessioncode).values()
        moderator = Moderators.objects.all().filter(session_code=x.sessioncode).values()


        context['moderator'] = moderator[0]['moderator_name']
        context['speaker'] = moderator[0]['speaker']

        context['startcount'] = session[0]['start_count']
        context['midcount'] = session[0]['mid_count']
        context['comments'] = session[0]['comments']

        context['message'] = 'OK'

        return JsonResponse(context, status=status.HTTP_200_OK)
    else:
        content = {
            'message': 'An error occured'
        }
        return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)

