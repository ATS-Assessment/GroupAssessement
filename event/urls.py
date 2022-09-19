from django.urls import path
from . import views
urlpatterns = [
    path('', views.AllEventsListView.as_view(), name='event-list'),
    path('calendar/<int:group_pk>/',
         views.CalendarViewNew.as_view(), name="calendar-view"),
    path('edit-event/<int:event_pk>/',
         views.edit_event, name="edit-event"),
    path('event-detail-gcal/<int:event_pk>/',
         views.ViewEvent.as_view(), name="event-detail-gcal"),
    path('yes/<int:group_pk>/<int:event_pk>/',
         views.yes_members_view, name="yes-members"),
    path('no/<int:group_pk>/<int:event_pk>/',
         views.no_members_view, name="no-members"),
    path('maybe/<int:group_pk>/<int:event_pk>/',
         views.maybe_members_view, name="maybe-members"),
<<<<<<< HEAD






=======
>>>>>>> origin
    # path('notifications/mark_all_read/',
    #      views.mark_all_read, name='mark_all_read'),
    # path('notifications/delete_all_read/',
    #      views.delete_all_read, name='delete_all_read'),
]