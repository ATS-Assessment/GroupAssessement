
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete, post_init

from notification.models import Notification


# Create your models here.


class ActiveManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class InactiveManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=False)


class ExitedManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(has_exited=True)


class SuspendedMember(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_suspended=True)


class NotSuspendedMember(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_suspended=False)


class Group(models.Model):
    PRIVACY_STATUS = (
        ("open", "Open"),
        ("closed", "Closed"),
    )
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    privacy_status = models.CharField(max_length=50, choices=PRIVACY_STATUS)
    group_image = models.ImageField(
        upload_to="groups/images", default="group.jpg")
    creator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="group_admin")
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    exited_objects = ExitedManager()
    inactive_objects = InactiveManager()

    def __str__(self) -> str:
        return self.name


class GroupRequest(models.Manager):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    request_message = models.CharField(max_length=100)
    date_sent = models.DateTimeField(auto_now_add=True)

    def member_requested(self):
        pass


class Member(models.Model):
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="group_member")
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=True)
    is_suspended = models.BooleanField(default=False)
    has_exited = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_members = ActiveManager()
    inactive_members = InactiveManager()
    suspended_members = SuspendedMember()
    not_suspended_members = NotSuspendedMember()


class Post(models.Model):
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    content = models.TextField()
    post_image = models.ImageField(
        upload_to="posts/images", blank=True, null=True)
    post_files = models.FileField(
        blank=True, upload_to="posts/files", null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InactiveManager()

    def member_post(self):
        pass


class Comment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InactiveManager()

    def member_commented(self):
        pass


class Replies(models.Model):
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InactiveManager()

    def member_replied(self):
        pass


class Like(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(
        Comment, blank=True, null=True, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, blank=True, null=True)
    reply = models.ForeignKey(
        Replies, blank=True, null=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InactiveManager()

    def member_like_post(sender, instance, *args, **kwargs):
        like = instance
        sender = like.member
        receiver = like.post

        notify = Notification.objects.create(sender=sender,
                                             receiver=receiver, notification_type=1)
