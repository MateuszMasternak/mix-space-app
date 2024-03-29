from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('log-in', views.log_in, name='log_in'),
    path('log-out', views.log_out, name='log_out'),
    path('upload', views.upload, name='upload'),
    path('user/<str:username>', views.show_user, name='user'),
    path('like/<int:pk>', views.like, name='like'),
    path('liked', views.liked, name='liked'),
    path('follow/<str:username>', views.follow, name='follow'),
    path('following', views.following, name='following'),
    path('music-player/<int:pk>', views.player, name='player'),
    path('search', views.search, name='search'),
    path('avatar-upload', views.avatar_upload, name='avatar_upload'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('delete/<int:pk>', views.delete, name='delete'),
]