from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from GrowexoAuction import settings
from Main import views
app_name="Main"
urlpatterns = [
    path('', views.Home, name='Home'),
    path('Login', views.Login, name='Login'),
    path('Logout', views.Logout, name='Logout'),
]