from django.urls import path, re_path

from ..views import views_login, views, views_add


urlpatterns = [
    path('', views.index, name='index'),

    path('login', views_login.login, name="login"),
    path('login.html', views_login.login, name="login"),
    path('logout', views_login.logout, name="logout"),


    path('index', views.index, name='index'),

    path('form', views.form_sample, name='form'),

    path('encode_values', views.encode_values, name='value'),
    path('moderator', views.moderator, name='moderator'),


    # ajax methods

    path('add_values', views_add.add_values, name='add_values'),
    #path('refresh_values', views.refresh_values, name='refresh_values'),


]