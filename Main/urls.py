from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from GrowexoAuction import settings
from Main import views

urlpatterns = [
    path('', views.Home, name='Home'),
]