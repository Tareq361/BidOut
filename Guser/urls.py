from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from GrowexoAuction import settings
from Guser import views
app_name="Guser"
urlpatterns = [
    path('SignUp', views.Signup, name='Signup'),
    path('Active', views.Active, name='Active'),
    path('forget-password', views.forget_password, name='forget_password'),
    path('reset_password/',views.reset_password,name='reset_password'),
    path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate,name='resetpassword_validate'),
]