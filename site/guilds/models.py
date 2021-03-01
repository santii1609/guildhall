import datetime

from django.db import models
from django.utils import timezone

class Guild(models.Model):

    name = models.CharField(max_length=200)
    creation_date = models.DateTimeField('date published')

    def __str__(self):
        return self.name

    def was_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.creation_date <= now

class Description(models.Model):

    guild = models.ForeignKey(Guild, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.guild.name + self.text
