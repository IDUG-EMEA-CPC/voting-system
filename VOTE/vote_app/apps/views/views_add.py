from django.template import loader
from django.shortcuts import redirect, render
from ..views.views_login import login
from ..score.utils import RequestParameters, retrieve_value_from_session, init_response_context
from ..score.models import Sessioneval, Session
from django.http import JsonResponse
from rest_framework import status

from ..tables.tables import SessionEvalTable
from django_tables2 import RequestConfig

from django.core.paginator import Paginator
from django.template.loader import render_to_string


def add_values(request):
    if request.user.is_authenticated:
        # retrieving parameters
        x = RequestParameters()  # generic class for request parameters

        for key in ['sessioncode', 'overall', 'speaker', 'material', 'expectation', 'name', 'company', 'comments' ]:
            setattr(x, key, retrieve_value_from_session(request, key))

        # trying to insert
        sessioncode_id = Session.objects.get(sessioncode=x.sessioncode)
        new_eval = Sessioneval(sessioncode=sessioncode_id,
                               overallrating=x.overall if x.overall else None,
                               speakerrating=x.speaker if x.speaker else None,
                               materialrating=x.material if x.material else None,
                               expectationrating=x.expectation if x.expectation else None,
                               atendeename=x.name if x.name else None,
                               company=x.company if x.company else None,
                               comments=x.comments if x.comments else None
                               )

        new_eval.save()

        context = init_response_context(request)
        context['message'] = 'OK'
        context['code'] = new_eval.overallrating

        return JsonResponse(context, status=status.HTTP_200_OK)



    else:
        return redirect(login)


def refresh_values(request):
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

        if 'encode_values' in x.url and 'page=' in x.url:
            pos = x.url.index('page=') + len('page=')
            page = x.url[pos:]
            eval_items = Sessioneval.objects.all().filter(sessioncode=x.sessioncode).order_by('-id')

            #paginator = Paginator(eval_items, 5)
            #items = paginator.get_page(page)

            evals = SessionEvalTable(eval_items)

            RequestConfig(request, paginate={"per_page": 5}).configure(evals)

            # paginator = Paginator(eval_items.page., 5)
            evals.page = evals.page.paginator.get_page(page)

        else:
            eval_items = Sessioneval.objects.all().filter(sessioncode=x.sessioncode).order_by('-id')



            #eval_items.paginator.get_page(1)

            evals = SessionEvalTable(eval_items)

            RequestConfig(request, paginate={"per_page": 5}).configure(evals)



        context['items'] = evals

        session = Session.objects.filter(sessioncode=x.sessioncode).first()
        session_title = session.sessiontitle if session else None

        request.session['session_code'] = x.sessioncode
        request.session['session_title'] = session_title

        return render(request, 'tables/table_sessioneval.html', {'items': evals})
    else:
        content = {
            'message': 'An error occured'
        }
        return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)


