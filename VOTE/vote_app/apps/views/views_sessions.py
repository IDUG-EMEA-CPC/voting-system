from django.template import loader
from django.shortcuts import redirect, render
from ..views.views_login import login
from ..score.utils import RequestParameters, retrieve_value_from_session, init_response_context
from ..score.models import Session
from django.http import JsonResponse
from rest_framework import status

from ..tables.tables import SessionTable
from django_tables2 import RequestConfig

from django.core.paginator import Paginator
from django.template.loader import render_to_string


def refresh_sessions(request):
    if not request.user.is_authenticated:
        print('out of session')
        content = {
            'message': 'Your session has expired. Please <a href="./login.html">login</a>'
        }
        return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        # retrieving parameters
        x = RequestParameters()  # generic class for request parameters

        for key in ['sessioncode', 'url']:
            setattr(x, key, retrieve_value_from_session(request, key))

        context = init_response_context(request)

        if 'sessions' in x.url and 'page=' in x.url:
            pos = x.url.index('page=') + len('page=')
            page = x.url[pos:]
            sessions_items = Session.objects.all().order_by('sessioncode')

            sessions = SessionTable(sessions_items)

            RequestConfig(request, paginate={"per_page": 13}).configure(sessions)

            sessions.page = sessions.page.paginator.get_page(page)

        else:
            sessions_items = Session.objects.all().order_by('sessioncode')

            sessions = SessionTable(sessions_items)

            RequestConfig(request, paginate={"per_page": 13}).configure(sessions)

        return render(request, 'tables/table_session.html', {'items': sessions})
    else:
        content = {
            'message': 'An error occured'
        }
        return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)

