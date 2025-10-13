from rest_framework import status
from django.shortcuts import redirect, render
from django.http import JsonResponse

from ..selection.models import Moderators, Moderator, Session
from ..selection.utils import init_response_context


def get_modal_edit_value(request):
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        is_mobile = request.headers.get('X-Mobile-View') == 'true'

        mod = Moderators.objects.all().filter(session_code=session_id)

        if len(mod) == 1:
            context = init_response_context(request)

            context.update({
                'session_id': session_id,
                'session_date': mod[0].session_date,
                'session_time': mod[0].session_time,
                'session_title': mod[0].session_title,
                'speaker': mod[0].speaker,
                'platform': mod[0].subject_desc,
                'moderator_name': mod[0].moderator_name,
            })

            # Optional: fetch moderator_email if it exists
            ses = Moderator.objects.filter(session_code=session_id).first()
            if ses:
                context['moderator_email'] = ses.moderator_email

            # Choose template
            template_name = (
                'modal/modal_value_edit_mobile.html'
                if is_mobile
                else 'modal/modal_value_edit.html'
            )

            return render(request, template_name, context)

        return JsonResponse({'message': 'An error occurred - No data'}, status=400)

    return JsonResponse({'message': 'An error occurred'}, status=400)


def update_modal_edit_value(request):
    if request.method == 'POST':
        session_id = request.POST.get('session_id')

        mod = Moderator.objects.all().filter(session_code=session_id)

        if len(mod) == 1:
            for i in mod:
                i.moderator_name = request.POST.get('moderator_name') if request.POST.get('moderator_name') != '' else None
                i.moderator_email = request.POST.get('moderator_email') if request.POST.get('moderator_email') != '' else None
                i.save()

            if request.POST.get('moderator_name') != '' or request.POST.get('moderator_email') != '':
                ses = Session.objects.all().filter(session_code=session_id)
                if len(ses) == 1:
                    for i in ses:
                        i.moderator_status_id = 1
                        i.save()
            else:
                ses = Session.objects.all().filter(session_code=session_id)
                if len(ses) == 1:
                    for i in ses:
                        i.moderator_status_id = 0
                        i.save()

                mod.delete()

            context = init_response_context(request)
            context['message'] = 'OK'

            return JsonResponse(context, status=status.HTTP_200_OK)
        else:
            if request.POST.get('moderator_name') != '' or request.POST.get('moderator_email') != '':
                mod = Moderator.objects.create(
                    session_event="EMEA2025",
                    session_code=session_id,
                    moderator_name = request.POST.get('moderator_name') if request.POST.get('moderator_name') != '' else None,
                    moderator_email = request.POST.get('moderator_email') if request.POST.get('moderator_email') != '' else None
                )


                ses = Session.objects.all().filter(session_code=session_id)
                if len(ses) == 1:
                    for i in ses:
                        i.moderator_status_id = 1
                        i.save()



            context = init_response_context(request)
            context['message'] = 'OK'

            return JsonResponse(context, status=status.HTTP_200_OK)
    else:
        content = {
            'message': 'An error occured'
        }
        return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)

