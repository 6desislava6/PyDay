from django.db import models


class Alarm(models.Model):
    user = models.ForeignKey(
        'pyday_social_network.PyDayUser',
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField()
    message = models.TextField(blank=True, default="PyDay :) PyDay")
# Create your models here.
