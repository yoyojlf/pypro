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
from photos.views import HomeView, DetailView, CreateView, PhotoListView, UserPhotosView
from users.views import LoginView, LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),

    #Photos URLs
#    url(r'^$', views_photos.home, name='photos_home'), #url normal basada en funcion
    url(r'^$', HomeView.as_view(), name='photos_home'), #url basada en clase
    url(r'^photos/$', PhotoListView.as_view(), name='photos_list'), #url normal basada en clase
    url(r'^my-photos/$', UserPhotosView.as_view(), name='user_photos'), #url normal basada en clase
#    url(r'^photos/(?P<pk>[0-9]+)$', views_photos.detail, name='photo_detail'), #url normal basada en funcion
    url(r'^photos/(?P<pk>[0-9]+)$', DetailView.as_view(), name='photo_detail'), #url normal basada en clase
#    url(r'^photos/new$', views_photos.create, name='create_photo'), #url normal basada en funcion
    url(r'^photos/new$', CreateView.as_view(), name='create_photo'), #url normal basada en clase


    #Users URLs
#    url(r'^login$', users_views.login, name='users_login'), #url normal basada en funcion
    url(r'^login$', LoginView.as_view(), name='users_login'), #url normal basada en clase
#    url(r'^logout$', users_views.logout, name='users_logout'), #url normal basada en funcion
    url(r'^logout$', LogoutView.as_view(), name='users_logout'), #url normal basada en clase
]

