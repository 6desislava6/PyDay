from django import forms
from pyday_social_network.models import PyDayUser


class UploadPictureForm(forms.Form):
    picture = forms.FileField(
        label='Select a profile picture',
    )


'''class RegisterUserForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.CharField(max_length=120)
'''


class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = PyDayUser
        fields = ['first_name', 'last_name', 'email', 'password']
        widgets = {'password': forms.PasswordInput()}


class LoginUserForm(forms.Form):
    email = forms.CharField(max_length=120)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        widgets = {'password': forms.PasswordInput()}
