"""SocialMediaApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import (handler400, handler404, handler403, handler500)

handler500 = "groups.views.page_500"
handler403 = "groups.views.page_403"
handler404 = "groups.views.page_404"
handler400 = "groups.views.page_400"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('group/', include('groups.urls')),

    path('notification/', include('notification.urls')),

    path('poll/', include('poll.urls')),
    path('event/', include('event.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
