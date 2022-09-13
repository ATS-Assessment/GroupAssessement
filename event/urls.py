from django.urls import path
from . import views

urlpatterns = [
    path('', views.AllEventsListView.as_view(), name='event-list'),
    path('calendar/',
         views.CalendarViewNew.as_view(), name="calendar-view"),
    # path('notifications/mark_all_read/',
    #      views.mark_all_read, name='mark_all_read'),
    # path('notifications/delete_all_read/',
    #      views.delete_all_read, name='delete_all_read'),

]
