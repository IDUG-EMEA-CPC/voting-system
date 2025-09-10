from rest_framework import status
from django.shortcuts import redirect, render
from django.http import JsonResponse

from ..selection.models import Moderators
from ..selection.utils import init_response_context


def get_modal_edit_value(request):
    if request.method == 'POST':
        sessioneval_id = request.POST.get('sessioneval_id')

        evals = Sessioneval.objects.all().filter(id=sessioneval_id)

        if len(evals) == 1:

            context = init_response_context(request)

            context['sessioneval_id'] = sessioneval_id

            context['overall'] = evals[0].overallrating
            context['speaker'] = evals[0].speakerrating
            context['material'] = evals[0].materialrating
            context['expectation'] = evals[0].expectationrating
            context['name'] = evals[0].atendeename
            context['company'] = evals[0].company
            context['comments'] = evals[0].comments

            return render(request, 'modal/modal_value_edit.html', context)
        else:
            content = {
                'message': 'An error occured - No data'
            }
            return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)
    else:
        content = {
            'message': 'An error occured - Not logged in'
        }
        return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)


def update_modal_edit_value(request):
    if request.method == 'POST':
        sessioneval_id = request.POST.get('sessioneval_id')

        evals = Sessioneval.objects.all().filter(id=sessioneval_id)

        if len(evals) == 1:

            for i in evals:
                i.overallrating = request.POST.get('overall') if request.POST.get('overall') != '' else None
                i.speakerrating = request.POST.get('speaker') if request.POST.get('speaker') != '' else None
                i.materialrating = request.POST.get('material') if request.POST.get('material') != '' else None
                i.expectationrating = request.POST.get('expectation') if request.POST.get('expectation') != '' else None
                i.atendeename = request.POST.get('name') if request.POST.get('name') != '' else None
                i.company = request.POST.get('company') if request.POST.get('company') != '' else None
                i.comments = request.POST.get('comments') if request.POST.get('comments') != '' else None
                i.save()

            context = init_response_context(request)
            context['message'] = 'OK'

            return JsonResponse(context, status=status.HTTP_200_OK)
        else:
            content = {
                'message': 'An error occured - No data'
            }
            return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)
    else:
        content = {
            'message': 'An error occured - Not logged in'
        }
        return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)


def get_modal_delete_value(request):
    if request.method == 'POST':
        sessioneval_id = request.POST.get('sessioneval_id')

        evals = Sessioneval.objects.all().filter(id=sessioneval_id)

        if len(evals) == 1:

            context = init_response_context(request)

            context['sessioneval_id'] = sessioneval_id

            context['overall'] = evals[0].overallrating
            context['speaker'] = evals[0].speakerrating
            context['material'] = evals[0].materialrating
            context['expectation'] = evals[0].expectationrating
            context['name'] = evals[0].atendeename
            context['company'] = evals[0].company
            context['comments'] = evals[0].comments

            return render(request, 'modal/modal_value_delete.html', context)
        else:
            content = {
                'message': 'An error occured - No data'
            }
            return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)
    else:
        content = {
            'message': 'An error occured - Not logged in'
        }
        return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)



def delete_modal_edit_value(request):
    if request.method == 'POST':
        sessioneval_id = request.POST.get('sessioneval_id')

        evals = Sessioneval.objects.all().filter(id=sessioneval_id)

        if len(evals) == 1:

            evals.delete()

            context = init_response_context(request)
            context['message'] = 'OK'

            return JsonResponse(context, status=status.HTTP_200_OK)
        else:
            content = {
                'message': 'An error occured - No data'
            }
            return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)
    else:
        content = {
            'message': 'An error occured - Not logged in'
        }
        return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)
