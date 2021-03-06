from django import forms
from pyday_calendar.models import Event


class CreateEventForm(forms.ModelForm):
    class Meta:
        model = Event
        # TODO - координатите
        fields = ['date', 'title', 'from_time', 'to_time', 'caption', 'importance']
        widgets = {'date': forms.DateInput(attrs={'id': 'datepicker'})}

# или SelectDateWidget


class MonthForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'id': 'datepicker'}))
