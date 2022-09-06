from django.urls import path
from . import views


urlpatterns = [
    path('create-group/<int:user_pk>/', views.create_group, name="create-group"),
    path('groups/', views.GroupList.as_view(), name="group-list"),
    path('make-admin/<int:admin_pk>/<int:user_pk>/',
         views.make_admin, name="make-admin"),

]
