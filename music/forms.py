from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.core.files.images import get_image_dimensions
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.forms import Form, ModelForm, ValidationError
from django.forms import CharField, EmailField, PasswordInput, Select
from .models import CustomAbstractUser as User, Track
import string


class SignUpForm(UserCreationForm):
    email = EmailField(required=True, label='Email')
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={'hl': 'en'}))

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2', 'captcha')

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).count() != 0:
            raise ValidationError('This email is unavailable.')

        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError('This email is incorrect.')

        return email
    
    def clean_username(self):
        username = self.cleaned_data['username']

        if len(username) < 5:
            raise ValidationError('This username is too short.')
        elif len(username) > 32:
            raise ValidationError('This username is too long.')

        signs = ''.join(string.ascii_letters + string.digits + '_')
        for sign in username:
            if sign not in signs:
                raise ValidationError('This username contain not allowed signs.')

        if User.objects.filter(username=username).count() != 0:
            raise ValidationError('This username is unavailable.')

        return username


class LogInForm(Form):
    login = CharField(max_length=320, required=True)
    password = CharField(widget=PasswordInput, required=True)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={'hl': 'en'}))


class UserAvatarForm(ModelForm):
    class Meta:
        model = User
        fields = ('avatar',)
    
    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            w, h = get_image_dimensions(avatar)

            max_width = max_height = 100
            if w > max_width or h > max_height:
                raise ValidationError(
                    u'Please use an image that is '
                    '%s x %s pixels or smaller.' % (max_width, max_height))

            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'png']):
                raise ValidationError(u'Please use a JPEG, or PNG image.')

            if len(avatar) > (10 * 1024):
                raise ValidationError(
                    u'Avatar file size may not exceed 10mb.')
        except AttributeError:
            return None

        return avatar


class AddSetForm(ModelForm):
    class Meta:
        model = Track
        fields = ('title', 'genre', 'file')
        GENRE_CHOICE = (
            ('', 'Select genre'),
            ('Techno', 'Techno'),
            ('Drum and bass', 'Drum and bass'),
            ('Jungle', 'Jungle'),
            ('House', 'House'),
        )
        widgets = {
            "genre": Select(choices=GENRE_CHOICE)
        }

    def clean_title(self):
        title = self.cleaned_data['title']

        if len(title) < 4:
            raise ValidationError('This title is too short.')
        elif len(title) > 32:
            raise ValidationError('This title is too long.')

        return title
