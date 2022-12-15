from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from GrowexoAuction import settings
from dashboard import views
app_name="dashboard"
urlpatterns = [
    path('dashboard/<slug:slug>', views.dashboard, name='mydashboard'),

]