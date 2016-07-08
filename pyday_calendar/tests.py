from django.test import TestCase
from pyday_calendar.models import Event, Participant, TimeEventException
from pyday_social_network.models import PyDayUser
from datetime import datetime
from pyday_calendar.forms import CreateEventForm
from unittest.mock import Mock
from pyday_calendar.views import *
from django.core.urlresolvers import reverse
from django.test import Client
from pyday_calendar.services import *


class EventTest(TestCase):

    def setUp(self):
        self.user = PyDayUser.objects._create_user("bla@bla.bla", "secret",
                                                   "MynameisWhat",
                                                   "MynameisWho")
        self.date_time = datetime.now()
        self.data = {'from_time': self.date_time.hour,
                     'to_time': self.date_time.hour + 1,
                     'importance': "important", 'caption': "",
                     'date': self.date_time, 'title': "title"}

    def test_create_event(self):
        form = Mock(cleaned_data=self.data)
        self.event = Event.objects.create_event(self.user, form)
        self.assertEqual(len(Event.objects.all()), 1)
        event = Event.objects.get(pk=1)
        self.assertEqual(event.from_time, self.date_time.hour)
        self.assertEqual(event.to_time, self.date_time.hour + 1)
        self.assertEqual(event.importance, "important")
        self.assertEqual(event.caption, "")
        self.assertEqual(event.date, self.date_time.date())
        self.assertEqual(event.title, "title")

    def test_create_event_wrong_to_time(self):
        wrong_data = {'from_time': self.date_time.hour,
                      'to_time': self.date_time.hour - 1,
                      'importance': "important", 'caption': "",
                      'date': self.date_time, 'title': "title"}
        form = Mock(cleaned_data=wrong_data)

        with self.assertRaises(TimeEventException):
            Event.objects.create_event(self.user, form)


class ParticipantTest(TestCase):
    def setUp(self):
        self.user = PyDayUser.objects._create_user("bla@bla.bla", "secret",
                                                   "MynameisWhat",
                                                   "MynameisWho")
        self.user_second = PyDayUser.objects._create_user("bla@bla.bla2",
                                                          "secret",
                                                          "MynameisWhat",
                                                          "MynameisWho")
        self.date_time = datetime.now()
        self.data = {'from_time': self.date_time.hour,
                     'to_time': self.date_time.hour + 1,
                     'importance': "important", 'caption': "",
                     'date': self.date_time, 'title': "title"}
        self.form = Mock(cleaned_data=self.data)
        self.user.follow(self.user_second.id)
        self.user_second.follow(self.user.id)

    def test_create_event_participants(self):
        Event.objects.create_event(self.user, self.form, [self.user_second.id])
        self.assertEqual(len(Participant.objects.all()), 1)
        self.assertEqual(Participant.objects.get(pk=1).participant_id,
                         self.user_second.id)
        self.assertEqual(Event.objects.get(pk=1).participants,
                         [self.user_second])


class EventViewTest(TestCase):

    def setUp(self):
        date_time = datetime.now()
        self.client = Client()
        self.user = PyDayUser.objects._create_user("bla@bla.bla", "secret",
                                                   "MynameisWhat",
                                                   "MynameisWho")

        self.event = Event(owner=self.user, from_time=date_time.hour,
                           to_time=date_time.hour + 1,
                           importance="important", caption="",
                           date=date_time, title="title")
        self.event.save()

    def test_event_display_not_logged(self):
        with self.assertTemplateUsed("error.html"):
            response = self.client.get("/social/event/")
            self.assertEqual(response.status_code, 200)

    def test_event_display_logged(self):
        self.client.login(email='bla@bla.bla', password='secret')
        with self.assertTemplateUsed("event.html"):
            response = self.client.get("/calendar/event/1")
            self.assertEqual(response.status_code, 200)

    def test_event_others(self):
        date_time = datetime.now()
        self.client.login(email='bla@bla.bla', password='secret')
        user_second = PyDayUser.objects._create_user("bla@bla.bla2", "secret",
                                                     "MynameisWhat",
                                                     "MynameisWho")
        Event(owner=user_second, from_time=date_time.hour,
              to_time=date_time.hour + 1,
              importance="important", caption="",
              date=date_time, title="title").save()
        with self.assertTemplateUsed("error.html"):
            response = self.client.get("/calendar/event/2")
            self.assertEqual(response.status_code, 200)


class MontlyEventViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = PyDayUser.objects._create_user("bla@bla.bla", "secret",
                                                   "MynameisWhat",
                                                   "MynameisWho")

    def test_get_not_logged(self):
        response = self.client.get(reverse("pyday_calendar:monthly_events"),
                                   follow=True)
        self.assertEqual(response.redirect_chain,
                         [('/social/register/?next=/calendar/monthly_events/', 302)])

    def test_get_logged(self):
        self.client.login(email='bla@bla.bla', password='secret')
        with self.assertTemplateUsed("monthly_event.html"):
            resp = self.client.get(reverse("pyday_calendar:monthly_events"))
            self.assertEqual(resp.status_code, 200)

    def test_post_wrong_date(self):
        self.client.login(email='bla@bla.bla', password='secret')
        with self.assertTemplateUsed("error.html"):
            self.client.post(reverse("pyday_calendar:monthly_events"), {
                             "date": "60/2016"})

    def test_post_right_date(self):
        self.client.login(email='bla@bla.bla', password='secret')
        with self.assertTemplateUsed("monthly_event.html"):
            self.client.post(reverse("pyday_calendar:monthly_events"), {
                             "date": "6/2016"})


class DailyEventViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = PyDayUser.objects._create_user("bla@bla.bla", "secret",
                                                   "MynameisWhat",
                                                   "MynameisWho")
        self.client.login(email='bla@bla.bla', password='secret')

    def test_get_wrong_date(self):
        with self.assertTemplateUsed("error.html"):
            response = self.client.get('/calendar/daily_events/6000/60/60')
            self.assertContains(response, 'Impossible date')

    def test_get_right_date(self):
        with self.assertTemplateUsed('daily_event.html'):
            response = self.client.get('/calendar/daily_events/6000/10/10')
            self.assertEqual(response.status_code, 200)

    def test_no_date(self):
        date = datetime.now()
        with self.assertTemplateUsed('daily_event.html'):
            response = self.client.get(reverse("pyday_calendar:daily_events"))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Events for {} ".format(date.day))


class CreateEventViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = PyDayUser.objects._create_user("bla@bla.bla", "secret",
                                                   "MynameisWhat",
                                                   "MynameisWho")
        self.client.login(email='bla@bla.bla', password='secret')

    def test_get(self):
        with self.assertTemplateUsed("create_event.html"):
            self.client.get(reverse("pyday_calendar:create_event"))

    def test_post_no_friends(self):
        response = self.client.post(reverse("pyday_calendar:create_event"),
                                    {'date': '07/01/2016',
                                     'title': "title", 'from_time': "1",
                                     'to_time': "2", 'caption': "",
                                     'importance': "important"}, follow=True)
        # TODO

class ServicesTest(TestCase):

    def test_make_hourly_events(self):
        date_time = datetime.now()
        user = PyDayUser.objects._create_user("bla@bla.bla", "secret",
                                              "MynameisWhat",
                                              "MynameisWho")
        event = Event(owner=user, from_time=1,
                      to_time=2,
                      importance="important", caption="",
                      date=date_time, title="title")
        event.save()
        event_second = Event(owner=user, from_time=6,
                             to_time=9,
                             importance="important", caption="",
                             date=date_time, title="title")
        event_second.save()
        hev = make_hourly_events(Event.objects.all(), 1)
        self.assertEqual(hev, [[event], [None], [None], [None], [None],
                               [event_second], [event_second], [event_second], [None],
                               [None], [None], [None], [None], [None], [None],
                               [None], [None], [None], [None],
                               [None], [None], [None], [None], [None]])

    def test_find_max_column(self):
        date_time = datetime.now()
        user = PyDayUser.objects._create_user("bla@bla.bla", "secret",
                                              "MynameisWhat",
                                              "MynameisWho")
        event = Event(owner=user, from_time=1,
                      to_time=2,
                      importance="important", caption="",
                      date=date_time, title="title")
        event_second = Event(owner=user, from_time=6,
                             to_time=9,
                             importance="important", caption="",
                             date=date_time, title="title")
        self.assertEqual(find_max_columns([event, event_second]), 1)
