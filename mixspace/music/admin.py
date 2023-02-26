from django.contrib import admin
from .models import CustomAbstractUser as User


admin.site.register(User)
