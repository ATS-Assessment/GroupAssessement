from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notification-list'),
    path('<int:noti_pk>/',
         views.notification_view, name="notification-detail"),
    path('notifications/mark_all_read/',
         views.mark_all_read, name='mark_all_read'),
    path('notifications/delete_all_read/',
         views.delete_all_read, name='delete_all_read'),

]
