from django.urls import path
from . import views


urlpatterns = [
    path('create-group/', views.create_group, name="create-group"),
    path('groups/', views.GroupList.as_view(), name="group-list"),
    path('groups/<int:group_pk>/', views.group_detail, name="group-detail"),
    path('make-admin/<int:admin_pk>/<int:user_pk>/',
         views.make_admin, name="make-admin"),
    path('groups/<int:group_pk>/<int:user_pk>/create-post', views.create_post, name="create-post"),

]
