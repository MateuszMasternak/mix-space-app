from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')
    
        def clean_username(self):
            username = self.cleaned_data["username"]

            if len(username) < 5:
                raise forms.ValidationError("This username is too short.")
            elif len(username) > 32:
                raise forms.ValidationError("This username is too long.")

            signs = "".join(string.ascii_letters + string.digits + "_")
            for sign in username:
                if sign not in signs:
                    raise forms.ValidationError('This username contain not allowed signs.')

            try:
                if User.objects.get(username=username):
                    raise forms.ValidationError("This username is is unavailable.")
            except User.DoesNotExist:
                pass

            return username

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            if User.objects.get(email=email):
                raise forms.ValidationError("This email is unavailable.")
        except User.DoesNotExist:
            pass

        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("This email is incorrect.")

        return email


class LogInForm(forms.Form):
    login = forms.CharField(max_length=320, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    