from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.
def Home(request):
    if request.user.is_authenticated:
        print("true")

    return render(request,"home.html")