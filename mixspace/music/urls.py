from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('log-in', views.log_in, name='log_in'),
    path('log-out', views.log_out, name='log_out'),
    path('upload', views.upload, name='upload'),
    path('user/<str:username>', views.show_user, name='user'),
    path('follow/<str:username>', views.follow, name='follow'),
    path('likes/<int:id>', views.likes, name='likes'),
    path('following', views.following, name='following')
]