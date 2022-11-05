from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from GrowexoAuction import settings
from Guser import views
app_name="Guser"
urlpatterns = [
    path('SignUp', views.Signup, name='Signup'),
    path('Active/<slug:slug>', views.Active, name='Active'),
]