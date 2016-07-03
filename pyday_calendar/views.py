from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from pyday_calendar.forms import CreateEventForm, MonthForm
from django.views.generic import View
from pyday.views import UploadView
from django.utils.decorators import method_decorator
from pyday_calendar.models import Event
from django.core.exceptions import ValidationError
from pyday_calendar.models import TimeEventException
from datetime import datetime
from pyday_calendar.services import make_hourly_events, find_max_columns, make_calendar
from pyday.settings import FORMAT_DATE


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
            calendar, month = make_calendar(date)
            events = Event.objects.filter(owner_id=owner_id,
                                          date__month=7)
        except ValueError:
            return render(request, 'error.html', {'error': 'Wrong date!'})
        else:
            return render(request, 'monthly_event.html',
                          {'calendar': calendar,
                           'events': str(events), 'month': month})


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
    def post(self, request):
        try:
            return super(CreateEventView, self).post(request)
        except ValidationError:
            # обработва грешката на отрицателните стойности
            return render(request, 'error.html', {'error': 'Negative hours!'})
        except TimeEventException:
            # to_time е преди from_time
            return render(request, 'error.html', {'error': 'The end of the event is before its start!'})
            pass
        except:
            pass


# TODO
# https://docs.djangoproject.com/en/1.9/topics/class-based-views/intro/
