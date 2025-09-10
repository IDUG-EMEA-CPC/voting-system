from django.urls import path, re_path

from ..views import views, views_modal


urlpatterns = [
    path('', views.moderator, name='index'),

    path('moderator', views.moderator, name='moderator'),


    # ajax methods

    path('refresh_moderators', views.refresh_moderators, name='refresh_moderators'),

    path('get_modal_edit_value', views_modal.get_modal_edit_value, name='get_modal_edit_value'),
    path('update_modal_edit_value', views_modal.update_modal_edit_value, name='update_modal_edit_value'),

]