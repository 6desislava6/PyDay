from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from pyday_calendar.forms import CreateEventForm
from django.views.generic import View
from pyday.views import UploadView
from django.utils.decorators import method_decorator
from pyday_calendar.models import Event, Participant
from pyday_social_network.models import PyDayUser
from django.core.exceptions import ValidationError
from pyday_calendar.models import TimeEventException
from datetime import datetime
from pyday_calendar.services import make_hourly_events, find_max_columns,make_calendar
from pyday.settings import FORMAT_DATE


class EventView(View):

    @method_decorator(login_required)
    def get(self, request, event_id):
        event = Event.objects.get(pk=event_id)
        if event.owner_id != request.user.id:
            return render(request, 'error.html', {'error': "Not permitted"})
        participants = list(map(lambda x: PyDayUser.objects.get(pk=x.participant_id),
                                Participant.objects.filter(event_id=event_id)))
        print(participants)
        return render(request, 'event.html', {'event': event, 'participants': participants})


class MontlyEventView(View):
    fail_url = '/social/error'

    @method_decorator(login_required)
    def get(self, request):
        date = datetime.now().strftime(FORMAT_DATE)
        return self._make_calendar(request, request.user.id, date)

    @method_decorator(login_required)
    def post(self, request):
        return self._make_calendar(request, request.user.id,
                                   request.POST['date'])

    def _make_calendar(self, request, owner_id, date):
        try:
            calendar, month, year = make_calendar(date)
        except ValueError:
            return render(request, 'error.html', {'error': 'Wrong date!'})
        else:
            return render(request, 'monthly_event.html',
                          {'calendar': calendar, 'month': month, 'year': year})


class DailyEventView(View):

    @method_decorator(login_required)
    def get(self, request, year, month, day):
        date_event = datetime(int(year), int(month), int(day))
        user = request.user
        events = Event.objects.filter(owner_id=user.id, date=date_event)
        hourly_events = make_hourly_events(events,
                                           find_max_columns(events) | 1)
        return render(request, 'daily_event.html',
                      {'hourly_events': enumerate(hourly_events)})


class CreateEventView(UploadView):
    form_class = CreateEventForm
    template_name = 'create_event.html'
    post_function = staticmethod(Event.objects.create_event)
    success_url = '/social/main'

    @method_decorator(login_required)
    def get(self, request):
        form = self.form_class()
        friends = request.user.friends
        return render(request, self.template_name, {'form': form, 'friends': friends})

    @method_decorator(login_required)
    def post(self, request):
        friends = request.POST.getlist('friends[]')
        try:
            return super(CreateEventView, self).post(request, friends)
        except ValidationError:
            # обработва грешката на отрицателните стойности
            return render(request, 'error.html', {'error': 'Negative hours!'})
        except TimeEventException:
            # to_time е преди from_time
            return render(request, 'error.html', {'error': 'The end of the event is before its start!'})
            pass

# TODO
# https://docs.djangoproject.com/en/1.9/topics/class-based-views/intro/
