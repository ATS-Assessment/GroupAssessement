from account.models import User
from django.db import models

from django.db import models
from django.db.models.signals import post_save, post_delete, post_init

from notification.models import Notification


# Create your models here.


class ActiveManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_hidden=False)


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


class GroupRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    request_message = models.CharField(max_length=100)
    date_sent = models.DateTimeField(auto_now_add=True)

    def member_join_request(sender, instance, *args, **kwargs):
        member_request = instance
        requester = member_request.user
        content_preview = member_request.request_message[:50]
        notify = Notification.objects.create(
            notification_type="group_request", is_admin_notification=True)
        notify.save()

    def member_withdraw_request(sender, instance, *args, **kwargs):
        member_request = instance
        requester = member_request.user
        content_preview = member_request.message[:50]
        notify = Notification.objects.filter(is_admin_notification=True)
        notify.save()


class Member(models.Model):
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="group_member")
    member = models.ForeignKey(
        User, related_name="user_member", on_delete=models.CASCADE)
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
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    content = models.TextField()
    post_image = models.ImageField(
        upload_to="posts/images", blank=True, null=True)
    post_files = models.FileField(
        blank=True, upload_to="posts/files", null=True)
    like = models.ManyToManyField(
        Member, related_name="post_liked_by", through="Like")
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_hidden = models.BooleanField(default=False)

    objects = models.Manager()
    visible_objects = ActiveManager()
    inactive_objects = InactiveManager()

    def member_post(self):
        pass


class Comment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=100)
    like = models.ManyToManyField(
        Member, related_name="comment_liked_by", through="Like")
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_hidden = models.BooleanField(default=False)

    objects = models.Manager()
    visible_objects = ActiveManager()
    inactive_objects = InactiveManager()

    def member_commented(sender, instance, *args, **kwargs):
        comment = instance
        post = comment.post
        receiver = comment.group
        text_preview = comment.body[:50]

        notify = Notification.objects.create(post=post, sender=sender, user=post.user,
                                             text_preview=text_preview, notification_type=2)
        notify.save()

    def member_del_comment(sender, instance, *args, **kwargs):
        comment = instance
        post = comment.post
        receiver = comment.group
        notify = Notification.objects.filter(
            receiver=receiver, sender=sender, notification_type=2)
        notify.delete()


# Comments signals stuff:
post_save.connect(Comment.member_commented, sender=Comment)
post_delete.connect(Comment.member_del_comment, sender=Comment)
pass


class Replies(models.Model):
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)
    content = models.TextField(max_length=80)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_hidden = models.BooleanField(default=False)

    objects = models.Manager()
    visible_objects = ActiveManager()
    inactive_objects = InactiveManager()

    def member_replied(self):
        pass


class Like(models.Model):
    member = models.ForeignKey(
        Member, related_name="liked_by", on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(
        Comment, related_name="comment_like", blank=True, null=True, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_like", blank=True, null=True)
    reply = models.ForeignKey(
        Replies, related_name="reply_like", blank=True, null=True, on_delete=models.CASCADE)
    group = models.ForeignKey(
        Group, related_name="like_group", on_delete=models.CASCADE, null=True, blank=True)
    date_liked = models.DateTimeField(auto_now_add=True)

    def member_like(sender, instance, *args, **kwargs):
        like = instance
        receiver = like.member
        object = like.post if like.post else like.comment

        notify = Notification.objects.create(
            receiver=receiver, notification_type="like")
        notify.save()

    def member_unlike(sender, instance, *args, **kwargs):
        unlike = instance
        receiver = unlike.member
        object = unlike.post if unlike.post else unlike.comment
        notify = Notification.objects.filter(
            receiver=receiver, notification_type="like")
        notify.delete()


post_save.connect(Like.member_like, sender=Like)
post_delete.connect(Like.member_unlike, sender=Like)
