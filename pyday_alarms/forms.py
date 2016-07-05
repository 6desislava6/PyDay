from django import forms
from pyday_alarms.models import Alarm


class CreateEventForm(forms.ModelForm):
    class Meta:
        model = Alarm
        fields = ['date', 'message']
        widgets = {'date': forms.DateInput(attrs={'id': 'datepicker'})}

