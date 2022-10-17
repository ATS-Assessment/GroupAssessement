import logging
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from account.models import User
from event.models import Event

# Create your models here.
logger = logging.getLogger(__name__)


class Notification(models.Model):
    NOTIFICATION_TYPE = (
        ("Like", "Like"),
        ("Group Request", "Group Request"),
        ("Event Invite", "Event Invite")
    )
    receiver = models.ForeignKey(
        "groups.Member", on_delete=models.SET_NULL, related_name="to_user", null=True)
    created_by = models.ForeignKey(
        "groups.Member", on_delete=models.CASCADE, related_name="noti_creator", null=True)
    group = models.ForeignKey(
        "groups.Group", on_delete=models.SET_NULL, null=True)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, null=True, blank=True)
    content_preview = models.CharField(max_length=100, null=True)
    notification_type = models.CharField(max_length=50,
                                         choices=NOTIFICATION_TYPE, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
    is_admin_notification = models.BooleanField(default=False)

<<<<<<< HEAD
    # yes = models.ManyToManyField("groups.Member", related_name="yes_members")
    # no = models.ManyToManyField("groups.Member", related_name="no_members")
    # maybe = models.ManyToManyField(
    #     "groups.Member", related_name="maybe_members")
    # not notpk userpk
    # Notification.objects.get(pk=notpk)
    # notif.yes.add(member.pk)
    # eventMember.objects.all()
    # Yes.
    # get evnt summary
    # Notification.objects.get(pk=notpk)
    # not
=======
>>>>>>> refs/remotes/origin/main
    def mark_as_seen(self) -> None:
        """Mark notification as viewed."""
        logger.info("Marking notification as viewed: %s" % self)
        self.is_seen = True
        self.save()

    def __str__(self):
        return self.notification_type

    class Meta:
        ordering = ["-time_created"]


class EventInvite(models.Model):
    event = models.ForeignKey(
        "event.Event", on_delete=models.CASCADE, null=True, blank=True)
    yes = models.ManyToManyField("groups.Member", related_name="yes_members", )
    no = models.ManyToManyField("groups.Member", related_name="no_members")
    maybe = models.ManyToManyField(
        "groups.Member", related_name="maybe_members")

    def __str__(self) -> str:
        return self.event.title

    def __str__(self) -> str:
        return self.event.title

# class Event(models.Model):
#     creator = models.ForeignKey("groups.Member", on_delete=models.SET_NULL, null=True)
#     group = models.ForeignKey(
#         "groups.Group", on_delete=models.SET_NULL, null=True)
#     title = models.CharField(max_length=100)
#     description = models.TextField(max_length=200)
#     date_created = models.DateTimeField(auto_now_add=True)
#     last_modified = models.DateTimeField(auto_now=True)
#    if notification_type == 'invite'
#        form
#     start_time = models.DateTimeField(null=True)
#     end_time = models.DateTimeField(null=True)
#     has_started = models.BooleanField(default=False)
#     start_date = models.DateTimeField(null=True)
#     end_date = models.DateTimeField(null=True)
#     def __str__(self) -> str:
#         return self.title
#     def has_started(self):
#         return self.start_date > datetime.datetime.now()
#     def admin_create_event(sender, instance, *args, **kwargs):
#         event = instance
#         sender = event.creator
#         receiver = event.group
#         notify = Notification.objects.create(group=receiver, created_by=sender)
#         notify.save()
<<<<<<< HEAD
# post_save.connect(Event.admin_create_event, sender=Event)
=======
>>>>>>> refs/remotes/origin/main
