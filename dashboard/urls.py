
from django.urls import path

from dashboard import views
app_name="dashboard"
urlpatterns = [
    path('dashboard/', views.user_dashboard, name='mydashboard'),
    path('dashboard/post-item/',views.PostItem,name="postItem")

]