from . import views
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
import django.contrib.auth.views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('about', views.about, name="about"),
    path('signup', views.signup, name='signup'),
    path('<int:pk>/inbox', views.inbox, name='inbox'),
    path('<int:upk>/new', views.new, name='new'),
    path('accounts/logout', views.logout_view, name="logout"),
    path('<int:upk>/inbox/<str:name>/inboxDetails', views.inboxDetails, name='inboxDetails'),
    path('<int:upk>/inbox/<str:name>/delete', views.delete, name='delete'),
    path('restricted', views.restricted, name="restricted"),
]
