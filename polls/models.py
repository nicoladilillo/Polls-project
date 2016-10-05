import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Poll(models.Model):
    title = models.CharField(max_length=40)
    pub_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title


class Question(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, null=True, blank=True)
    question_text = models.CharField(max_length=200)

    SINGLE = 'S'
    MULTIPLE = 'M'
    OPEN = 'O'
    TYPE_CHOICES = (
        ('SINGLE', 'Single'),
        ('MULTIPLE', 'Multiple'),
        ('OPEN', 'Open'),
    )
    choice_type = models.CharField(
        max_length=8,
        choices=TYPE_CHOICES,
        default=SINGLE,
    )

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Voter(models.Model):
    user = models.ForeignKey(User)
    poll = models.ForeignKey(Poll)
