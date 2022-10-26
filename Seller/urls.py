from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from GrowexoAuction import settings
from Seller import views
app_name="Seller"
urlpatterns = [
    path('/SignUp', views.Signup, name='Signup'),
]