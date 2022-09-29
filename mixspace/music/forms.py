from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')


class LogInForm(forms.Form):
    login = forms.CharField(max_length=320, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    