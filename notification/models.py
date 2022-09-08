from django.db import models
from account.models import User

# Create your models here.


def _json():
    return dict


def __json():
    return list


class Notification(models.Model):
    NOTIFICATION_TYPE = (
        (1, "like"),
        (2, "comment"),
        (3, "post"),
        (4, "group_request")
    )
    receiver = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="to_user", null=True)
    group = models.ForeignKey(
        "groups.Group", on_delete=models.SET_NULL, null=True)
    content_preview = models.CharField(max_length=100)
    notification_type = models.IntegerField(
        choices=NOTIFICATION_TYPE)
    time_created = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
    is_admin_notification = models.BooleanField(default=True)


class Event(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(
        "groups.Group", on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    # yes = models.JSONField(default=__json())
    # no = models.JSONField(default=__json())
    # maybe = models.JSONField(default=__json())

    def event():
        pass


class Poll(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(
        "groups.Group", on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=90, null=True)

