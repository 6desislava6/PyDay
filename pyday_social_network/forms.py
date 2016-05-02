from django import forms


class UploadPictureForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.CharField(max_length=120)
    file = forms.FileField(
        label='Select a profile picture',
    )

