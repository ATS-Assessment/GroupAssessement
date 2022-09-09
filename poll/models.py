from django.db import models

# Create your models here.
from account.models import User
from groups.models import Member


class Poll(models.Model):
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(
        "groups.Group", on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=90, null=True)
    start_date = models.DateTimeField(null=True)

    # # polls_option = models.JSONField(default=_json())
    #
    # def has_started(self):
    #     return self.start_date > datetime.datetime.now()


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    vote = models.IntegerField(default=0)


class Voter(models.Model):
    poll = models.ManyToManyField(Poll)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
