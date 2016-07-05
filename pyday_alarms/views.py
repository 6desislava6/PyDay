from django.shortcuts import render
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from pyday_alarms.services import update_alarms
from pyday_alarms.forms import CreateAlarmForm
from pyday_calendar.forms import CreateEventForm
from pyday_alarms.models import Alarm
from datetime import datetime, timedelta


class AlarmView(View):

    @method_decorator(login_required)
    def get(self, request):
        # да излизат всички аларми?
        form_alarm = CreateAlarmForm()
        return render(request, 'create_alarm.html', locals())

    # It creates a new alarm and updates all on the raspberry
    @method_decorator(login_required)
    def post(self, request):
        form = CreateEventForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            date = form['date'] + timedelta(hours=int(request.POST["hour"]),
                                            minutes=int(request.POST["mins"]))
            Alarm(user=request.user, message=form['message'], date=date).save()
            update_alarms(request.user)
            return HttpResponseRedirect('/social/main')
        else:
            return render(request, 'error.html', {'error': "Invalid form."})
