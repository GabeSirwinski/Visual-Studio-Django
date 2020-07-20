from . import views
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('about', views.about, name="about"),
    path('signup', views.signup, name='signup'),
]
