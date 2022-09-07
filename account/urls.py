from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('changepassword/', views.ChangePasswordView.as_view(), name='change-password'),
    path('update-profile/<int:pk>', views.UpdateProfileView.as_view(), name='update-profile'),
    # path('join-group/<int:pk>/<int:grouppk>/', views.MemberJoinGroupView.as_view(), name='join-group'),
    # path('<int:pk>/', views.MemberListView.as_view(), name='member-list'),
]
