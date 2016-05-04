from django import forms
from pyday_social_network.models import PyDayUser


class UploadPictureForm(forms.Form):
    picture = forms.FileField(
        label='Select a profile picture',
    )


class UploadSongForm(forms.Form):
    song = forms.FileField(
        label='Upload a song',
    )


class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = PyDayUser
        fields = ['first_name', 'last_name', 'email', 'password']
        widgets = {'password': forms.PasswordInput()}


class LoginUserForm(forms.Form):
    required_css_class = 'required'
    email = forms.CharField(max_length=120)
    password = forms.CharField(widget=forms.PasswordInput())
