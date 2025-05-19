from django.template import loader
from django.shortcuts import redirect, render
from ..views.views_login import login
from ..score.utils import RequestParameters, retrieve_value_from_session, init_response_context
from ..score.models import Session, Sessionmoderator
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

        session = Session.objects.all().filter(sessioncode=x.sessioncode).values()
        moderator = Sessionmoderator.objects.all().values()


        context['moderator'] = ''
        context['speaker'] = session[0]['primarypresenterfullname']
        context['startcount'] = '' #moderator[0]['startcount']
        context['midcount'] = '' #moderator[0]['midcount']

        context['message'] = 'OK'

        return JsonResponse(context, status=status.HTTP_200_OK)
    else:
        content = {
            'message': 'An error occured'
        }
        return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)

