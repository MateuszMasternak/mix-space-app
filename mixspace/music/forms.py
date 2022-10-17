from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.core.files.images import get_image_dimensions
from django.forms import ModelForm
from django import forms
from .models import User, Set
import string


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

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


class LogInForm(forms.Form):
    login = forms.CharField(max_length=320, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


class UserAvatarForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('avatar',)
    
    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            w, h = get_image_dimensions(avatar)

            max_width = max_height = 100
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                    '%s x %s pixels or smaller.' % (max_width, max_height))

            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, or PNG image.')

            if len(avatar) > (10 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 10mb.')
        except AttributeError:
            pass

        return avatar


class AddSetForm(ModelForm):
    class Meta:
        model = Set
        fields = ("title", "genre", "file")
        GENRE_CHOICE = (
            ("", "Select genre"),
            ("Techno", "Techno"),
            ("Drum and bass", "Drum and bass"),
        )
        widgets = {
            "genre": forms.Select(choices=GENRE_CHOICE)
        }

    def clean_title(self):
        title = self.cleaned_data["title"]

        if len(title) < 4:
            raise forms.ValidationError("This title is too short.")
        elif len(title) > 32:
            raise forms.ValidationError("This title is too long.")

        return title
