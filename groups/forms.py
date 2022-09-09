
from .models import Comment, Group, Post, Replies
from django import forms


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name", "description", "privacy_status", "group_image"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "post_image", "post_files"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content", ]


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Replies
        fields = ["content", ]
