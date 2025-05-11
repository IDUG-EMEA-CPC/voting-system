from django.template import loader
from django.shortcuts import redirect, render
from ..views.views_login import login
from ..score.utils import RequestParameters, retrieve_value_from_session, init_response_context
from ..score.models import Sessioneval, Session
from django.http import JsonResponse
from rest_framework import status


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


