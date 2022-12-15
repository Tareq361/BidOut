from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from Guser.models import GUser
from Item.models import *

# Create your views here.
def Home(request):
    context={}
    if request.user.is_authenticated:
        context['guser']=GUser.check_user(request.user)

    items=Item.objects.all().filter(status='Active');
    print(items)
    context['items']=items
    return render(request,"home.html",context)





def Login(request):
    if request.user.is_authenticated:
        print("true")

        return redirect('/')
    else :
        if request.method == "POST":
            print("success")
            userName = request.POST.get('user_name')
            pass1 = request.POST.get('password')
            user = authenticate(request, username=userName, password=pass1)
            if user is None:
                print("no user")
                messages.info(request, "User doesn't exist")
                return redirect('Main:Login')
                # if GUser.user_exist(userName,pass1):
                #     user=GUser.get_user(userName,pass1)
                #
                # else:
                #     messages.info(request, "Password doesn't match")
                #     return redirect('Main:Login')
            else:
                login(request, user)
                print("user")
                if request.POST.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('Main:Home')
        return render(request,"login.html")



@login_required
def Logout(request):
    logout(request);
    return redirect('/')