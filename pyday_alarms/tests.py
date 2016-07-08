from django.test import TestCase
from pyday_calendar.models import Event
from pyday_social_network.models import PyDayUser
from django.test import Client
from django.core.urlresolvers import reverse
from pyday_alarms.views import *
from datetime import datetime


class AlarmViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = PyDayUser.objects._create_user("bla@bla.bla", "secret",
                                                   "MynameisWhat",
                                                   "MynameisWho")
        self.client.login(email='bla@bla.bla', password='secret')

    def test_get(self):
        with self.assertTemplateUsed("create_alarm.html"):
            self.client.get(reverse("pyday_alarms:alarms"))

    def test_post(self):
        with self.assertTemplateUsed("error.html"):
            response = self.client.post(reverse("pyday_alarms:alarms"),
                                        {'date': '07/01/2016', 'hour': '1',
                                         'mins': '0', 'message': 'haha'},
                                        follow=True)
            self.assertContains(response, "Raspberry!")

    def test_post_invalid_form(self):
        with self.assertTemplateUsed("error.html"):
            response = self.client.post(reverse("pyday_alarms:alarms"), {})
            self.assertContains(response, "Invalid form")


