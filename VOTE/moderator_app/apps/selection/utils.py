import datetime

def init_response_context(request):
    first_login = False

    if request.user.is_authenticated:
        user = request.user
        if user.date_joined > user.last_login - datetime.timedelta(minutes=2):
            first_login = True


    context = {
        'user_info': {
            'id' : str(request.user),
            'last_name': request.user.last_name if request.user.is_authenticated else None,
            'first_name': request.user.first_name if request.user.is_authenticated else None,
            'first_login': first_login,
        },
        'user_permissions': {
            'can_request_new_data': request.user.has_perm('tagsgen.owner'),
            'can_edit': request.user.has_perm('tagsgen.editor'),
            'can_create': request.user.has_perm('tagsgen.editor'),
            'can_view': request.user.has_perm('tagsgen.visitor'),
        }
    }
    return context



def retrieve_value_from_session(request, key):
    try:
        value = request.POST[key]
    except Exception as e:
        print('missing', str(e))
        value = None

    return value


class RequestParameters(object):
    pass