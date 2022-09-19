from django.db import models
from django.utils import timezone

# Create your models here.
from account.models import User
from groups.models import Member, Group


class Poll(models.Model):
    creator = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=90, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ["-created_date"]


    def __str__(self):
        return self.title


    # # polls_option = models.JSONField(default=_json())
    #
    # def has_started(self):
    #     return self.start_date > datetime.datetime.now()


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200, null=True, blank=True)
    vote = models.IntegerField(default=0)


class Voter(models.Model):
    poll = models.ManyToManyField(Poll)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return self.member.member.email
