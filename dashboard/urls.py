
from django.urls import path

from dashboard import views
app_name="dashboard"
urlpatterns = [
    path('dashboard/<slug:slug>', views.UserDashboard.as_view(), name='mydashboard'),
    path('dashboard/post-item/',views.PostItem,name="postItem")

]