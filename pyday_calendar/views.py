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
from pyday_calendar.services import make_hourly_events, find_max_columns, make_calendar
from pyday.settings import FORMAT_DATE, MONTHS
from django.template import Context


class EventView(View):

    @method_decorator(login_required)
    def get(self, request, event_id):
        event = Event.objects.get(pk=event_id)
        if event.owner_id != request.user.id:
            return render(request, 'error.html', {'error': "Not permitted"})
        participants = event.participants
        return render(request, 'event.html',
                      {'event': event, 'participants': participants,
                       'user_request': request.user})


class MontlyEventView(View):
    fail_url = '/social/error'
    form_class = CreateEventForm

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
                          {**locals(), 'user_request': request.user,
                           'month_readable': MONTHS[month]})


class DailyEventView(View):
    form_class = CreateEventForm

    # Without any parameters in the url it returns the events for the current
    # day. Otherwise it returns the events for the given date

    @method_decorator(login_required)
    def get(self, request, year=None, month=None, day=None):
        try:
            form = self.form_class(initial={'date': datetime.now()})
            friends = request.user.friends
            date_event = self._make_date_event(year, month, day)
        except ValueError:
            return render(request, 'error.html', {'error': 'Impossible date'})
        else:
            user = request.user
            events = Event.objects.filter(owner_id=user.id, date=date_event)
            hourly_events = make_hourly_events(events,
                                               find_max_columns(events) | 1)
            return render(request, 'daily_event.html',
                          {'hourly_events': enumerate(hourly_events),
                           'user_request': request.user, 'form': form,
                           'friends': friends, 'day': date_event.day,
                           'month': MONTHS[date_event.month],
                           'year': date_event.year})

    def _make_date_event(self, year, month, day):
        if not year:
            return datetime.now()
        else:
            return datetime(int(year), int(month), int(day))


class CreateEventView(UploadView):
    form_class = CreateEventForm
    template_name = 'create_event.html'
    post_function = staticmethod(Event.objects.create_event)
    success_url = '/calendar/daily_events'

    @method_decorator(login_required)
    def get(self, request):
        form = self.form_class()
        friends = request.user.friends
        return render(request, self.template_name, {'form': form,
                                                    'friends': friends,
                                                    'user_request': request.user})

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

