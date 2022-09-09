from django.urls import path
from . import views


urlpatterns = [
    path('create-group/', views.create_group, name="create-group"),
    path('groups/', views.GroupList.as_view(), name="group-list"),
    path('groups/<int:group_pk>/', views.group_detail, name="group-detail"),
    path('make-admin/<int:admin_pk>/<int:user_pk>/',
         views.make_admin, name="make-admin"),
    path('request-to-join/<int:group_pk>/',
         views.request_to_join_group, name="request-to-join"),
    path('accept-request/', views.accept_to_group, name="accept-request"),
    path('remove-group-member/<int:group_pk>/<int:admin_pk>/<int:user_pk>/',
         views.remove_group_member, name="remove-group-member"),
    path('search/', views.search_groups, name="search-groups"),
    path('comment/<int:post_pk>/', views.comment_on_post, name="comment-on-post"),
    path('reply/<int:comment_pk>/', views.reply_comment, name="reply-comment"),
    path('like-post/', views.like_post, name="like-post"),
    path('like-comment/', views.like_comment, name="like-comment"),
    path('groups/<int:group_pk>/<int:user_pk>/create-post',
         views.create_post, name="create-post"),
]
