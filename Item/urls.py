

from django.urls import path, include

from GrowexoAuction import settings
from dashboard import views
app_name="Item"
urlpatterns = [
    path('Item/', views.dashboard, name='item'),

]