from django.db import models
from datetime import datetime
from account.models import User
# from notification.models import Notification
from django.db.models.signals import post_save, post_delete
from django.urls import reverse
# Create your models here.
class EventManager(models.Manager):
    """ Event manager """
    def get_all_events(self, group_pk):
        return Event.objects.filter(
            group__pk=group_pk)
    def get_running_events(self, member):
        return Event.objects.filter(
            member=member,
            end_time__gte=datetime.now().date(),
        ).order_by("start_time")
class EventAbstract(models.Model):
    """ Event abstract model """
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
class Event(EventAbstract):
    """ Event model """
    group = models.ForeignKey(
        "groups.Group", on_delete=models.CASCADE, related_name="event_group", null=True, blank=True)
    member = models.ForeignKey(
        "groups.Member", on_delete=models.SET_NULL, related_name="event_members", null=True, blank=True)
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    location = models.CharField(max_length=200, blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    objects = EventManager()
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("event-detail-gcal", args=(self.pk,))
    # def admin_create_event(sender, instance, *args, **kwargs):
    #     event = instance
    #     sender = event.member.member
    #     receiver_group = event.group
    #     notify = Notification.objects.create(
    #         group=receiver_group, content_preview="The Group Admin  Created an Event", is_admin_notification=False, created_by=sender)
    #     notify.save()
# post_save.connect(Event.admin_create_event, sender=Event)
class EventMember(EventAbstract):
    """ Event member model """
    # event = models.ForeignKey(
    #     Event, on_delete=models.CASCADE, related_name="event", null=True, blank=True)
    # member = models.ForeignKey(
    #     Member, on_delete=models.CASCADE, related_name="event_members", null=True, blank=True
    # )
    # group = models.ForeignKey(
    #     Group, on_delete=models.CASCADE, related_name="event_group", null=True, blank=True)
    def __str__(self):
        return str(self.user)