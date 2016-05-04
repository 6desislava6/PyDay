from django import forms
from pyday_calendar import Event


class CreateEventForm(forms.ModelForm):
    class Meta:
        model = Event
        # TODO - координатите
        fields = ['date', 'from_time', 'to_time', 'caption', 'importance']
