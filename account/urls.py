from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('creategroup/', views.CreatGroupView.as_view(), name='group'),
    path('add-to-admin/', views.AddAdminView.as_view(), name='addtoadmin'),
    path('remove-group-member/', views.RemoveMemberOfTheGroup.as_view(), name='remove-member'),
    path('grouplist/', views.GroupListView.as_view(), name='group-list'),
    path('changepassword/', views.ChangePasswordView.as_view(), name='change-password'),
    path('update-profile/<int:pk>', views.UpdateProfileView.as_view(), name='update-profile'),
    path('join-group/<int:pk>/<int:grouppk>/', views.MemberJoinGroupView.as_view(), name='join-group'),
    path('<int:pk>/', views.MemberListView.as_view(), name='member-list'),
]