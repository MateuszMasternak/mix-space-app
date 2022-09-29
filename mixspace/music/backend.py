from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .models import User
 

class CustomUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(
                User.USERNAME_FIELD,
                kwargs.get(User.EMAIL_FIELD))
        if username is None or password is None:
            return
        
        try:
            user = User._default_manager.get(
                Q(username__exact=username) | (Q(email__iexact=username) & Q(email_verified=True))
            )
        except User.DoesNotExist:
            # #20760
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user