from django.contrib import admin
from .models import CustomAbstractUser as User, Follow, Track, Like


admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Track)
admin.site.register(Like)
