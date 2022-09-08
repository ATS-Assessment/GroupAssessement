from django.urls import path
from . import views

urlpatterns = [
    path('edit-event/<int:event_pk>/', views.edit_event, name="edit-event"),
    path('create-event/', views.create_event, name="create-event"),
    path(),
]
