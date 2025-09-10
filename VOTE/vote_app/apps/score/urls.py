from django.urls import path, re_path

from ..views import views_login, views, views_add, views_modal, views_sessions, views_moderator


urlpatterns = [
    path('', views.index, name='index'),

    path('login', views_login.login, name="login"),
    path('login.html', views_login.login, name="login"),
    path('logout', views_login.logout, name="logout"),


    path('index', views.index, name='index'),
    path('sessions', views.sessions, name='form'),
    path('encode_values', views.encode_values, name='value'),
    path('encode_moderator', views.moderator, name='moderator'),


    # ajax methods

    path('add_values', views_add.add_values, name='add_values'),
    path('refresh_values', views_add.refresh_values, name='refresh_values'),

    path('get_modal_edit_value', views_modal.get_modal_edit_value, name='get_modal_edit_value'),
    path('update_modal_edit_value', views_modal.update_modal_edit_value, name='update_modal_edit_value'),

    path('get_modal_delete_value', views_modal.get_modal_delete_value, name='get_modal_delete_value'),
    path('delete_modal_edit_value', views_modal.delete_modal_edit_value, name='delete_modal_edit_value'),


    path('refresh_sessions', views_sessions.refresh_sessions, name='refresh_sessions'),

    path('refresh_moderator', views_moderator.refresh_moderator, name='refresh_moderator'),



]