from django.db import models
from pyday.settings import IMPORTANCE_CHOICES
from pyday_social_network.models import PyDayUser
from django.contrib.auth.models import BaseUserManager


class EventManager(BaseUserManager):
    def create_event():
        # раздробява датата блабла
        pass

    def create_event_request(request):
        pass


class Event(models.Model):
    owner = models.ForeignKey('pyday_social_network.PyDayUser', on_delete=models.CASCADE)
    date = models.DateField()
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    from_time = models.IntegerField()
    to_time = models.IntegerField()
    caption = models.TextField(blank=True)
    importance = models.CharField(max_length=20, choices=IMPORTANCE_CHOICES, default='1')
    coordinates = models.CharField(max_length=60, blank=True)
    objects = EventManager()

    @property
    def participants(self):
        event = Participant.object.all().filter(event=self)
        return [participant_event.event for participant_event in event]


class Participant(models.Model):
    participant = models.OneToOneField(PyDayUser)
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
