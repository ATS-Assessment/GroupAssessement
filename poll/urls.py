from django.urls import path
from . import views

app_name = 'poll'

urlpatterns = [
    path('<int:pk>/create/', views.create_poll, name='create-poll'),
    path('<int:pk>/vote/', views.vote, name='vote'),
    path('<int:group_pk>/<int:poll_pk>/edit/', views.edit_poll, name='edit'),
    path('<int:pk>/<int:poll_pk>/detail/', views.poll_detail, name='poll-detail'),
    path('<int:group_pk>/<int:poll_pk>/summary/', views.poll_summary, name='poll-summary'),
]
