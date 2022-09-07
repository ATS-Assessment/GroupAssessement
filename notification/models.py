from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models .signals import post_save, post_delete

from account.models import User


# Create your models here.


def _json():
    return dict


def __json():
    return list


class Notification(models.Model):
    NOTIFICATION_TYPE = (
        ("like", "like"),
        ("comment", "comment"),
        ("post", "post"),
        ("group_request", "group_request"),
        ("invite", "invite")
    )
    receiver = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="to_user", null=True)
    # admin_receiver = models.ForeignKey(
    #     User, on_delete=models.SET_NULL, related_name="to_user", null=True)
    group = models.ForeignKey(
        "groups.Group", on_delete=models.SET_NULL, null=True)
    content_preview = models.CharField(max_length=100, null=True)
    notification_type = models.IntegerField(
        choices=NOTIFICATION_TYPE, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
    is_admin_notification = models.BooleanField(default=False)


class Event(models.Model):
    EVENT_RESPONSE = (
        ("yes", "Yes"),
        ("no", "No"),
        ("maybe", "Maybe"),
    )
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(
        "groups.Group", on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    has_started = models.BooleanField(default=False)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    response = models.CharField(
        max_length=50, choices=EVENT_RESPONSE, blank=True, null=True)

    def has_started(self):
        return self.start_date > datetime.datetime.now()

    def admin_create_event(sender, instance, *args, **kwargs):
        event = instance
        sender = event.creator
        receiver = event.group
        notify = Notification.objects.create(receiver=receiver,)
        notify.save()


post_save.connect(Event.admin_create_event, sender=Event)


class Poll(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(
        "groups.Group", on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=90, null=True)
    polls_option = models.JSONField(default=_json())

    def has_started(self):
        return self.start_date > datetime.datetime.now()
