from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('log-in', views.log_in, name='log_in'),
    path('log-out', views.log_out, name='log_out'),
    path('show-user', views.show_user, name='show_user'),
    path('show-tracks', views.show_tracks, name='show_tracks'),
]