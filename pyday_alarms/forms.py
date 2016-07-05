from django import forms
from pyday_alarms.models import Alarm
from pyday_calendar.forms import CreateEventForm


class CreateAlarmForm(forms.ModelForm):
    class Meta:
        model = Alarm
        fields = ['date', 'message']
        widgets = {'date': forms.DateInput(attrs={'id': 'datepicker2'})}
