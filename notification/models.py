import logging
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models .signals import post_save, post_delete

from account.models import User


# Create your models here.
logger = logging.getLogger(__name__)


def _json():
    return dict


def __json():
    return list


class Notification(models.Model):
    NOTIFICATION_TYPE = (
        ("like", "like"),
        # ("comment", "comment"),
        # ("post", "post"),
        ("group_request", "group_request"),
        ("invite", "invite")
    )
    receiver = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="to_user", null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="noti_creator", null=True)
    group = models.ForeignKey(
        "groups.Group", on_delete=models.SET_NULL, null=True)
    content_preview = models.CharField(max_length=100, null=True)
    notification_type = models.CharField(max_length=50,
                                         choices=NOTIFICATION_TYPE, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
    is_admin_notification = models.BooleanField(default=False)
    yes = models.ManyToManyField("groups.Member", related_name="yes_members")
    no = models.ManyToManyField("groups.Member", related_name="no_members")
    maybe = models.ManyToManyField(
        "groups.Member", related_name="maybe_members")

    def mark_as_seen(self) -> None:
        """Mark notification as viewed."""
        logger.info("Marking notification as viewed: %s" % self)
        self.is_seen = True
        self.save()

    def __str__(self) -> str:
        return self.notification_type

    class Meta:
        ordering = ["-time_created"]


class Event(models.Model):
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

    def __str__(self) -> str:
        return self.title

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
    # polls_option = models.JSONField(default=_json())

    def has_started(self):
        return self.start_date > datetime.datetime.now()
