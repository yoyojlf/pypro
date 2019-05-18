"""frikr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from photos import views as views_photos
from users import views as users_views
urlpatterns = [
    path('admin/', admin.site.urls),

    #Photos URLs
    url(r'^$', views_photos.home, name='photos_home'),
    url(r'^photos/(?P<pk>[0-9]+)$', views_photos.detail, name='photo_detail'),
    url(r'^photos/new$', views_photos.create, name='create_photo'),

    #Users URLs
    url(r'^login$', users_views.login, name='users_login'),
    url(r'^logout$', users_views.logout, name='users_logout'),
]

