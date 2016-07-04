from django.db import models
from pyday.settings import IMPORTANCE_CHOICES
from pyday_social_network.models import PyDayUser
from django.contrib.auth.models import BaseUserManager
from pyday_calendar.validators import validate_range


class TimeEventException(Exception):
    pass


class EventManager(BaseUserManager):
    def create_event(self, user, form, friends=None):
        form = form.cleaned_data
        if form['to_time'] < form['from_time']:
            raise TimeEventException

        event = Event(owner=user, from_time=form['from_time'],
                      to_time=form['to_time'],
                      importance=form['importance'], caption=form['caption'],
                      date=form['date'], title=form['title'])
        event.save()
        self._add_participants(event, friends)

    def _add_participants(self, event, friends):
        if friends:
            for friend in friends:
                participant = PyDayUser.objects.get(pk=int(friend))
                print(participant)
                print(event)
                Participant(participant=participant, event=event).save()


class Event(models.Model):
    # Координати

    title = models.CharField(blank=False, max_length=60, default='')
    owner = models.ForeignKey('pyday_social_network.PyDayUser',
                              on_delete=models.CASCADE)
    date = models.DateField()
    from_time = models.IntegerField(validators=[validate_range(1, 24)])
    to_time = models.IntegerField(validators=[validate_range(1, 24)])
    caption = models.TextField(blank=True)
    importance = models.CharField(max_length=20, choices=IMPORTANCE_CHOICES,
                                  default='1')
    coordinates = models.CharField(max_length=60, blank=True)
    objects = EventManager()

    @property
    def participants(self):
        event = Participant.object.all().filter(event=self)
        return [participant_event.event for participant_event in event]

    def __str__(self):
        return "{} from {} to {} on {}".format(self.title, self.from_time, self.to_time, self.date)


class Participant(models.Model):
    participant = models.ForeignKey(
        'pyday_social_network.PyDayUser',
        on_delete=models.CASCADE,
    )
    event = models.ForeignKey('pyday_calendar.Event', on_delete=models.CASCADE)
