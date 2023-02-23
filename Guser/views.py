from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from .models import GUser
# Create your views here.
@csrf_protect
def Signup(request):
    phoneNo=''
    if request.user.is_authenticated:
        print('true user')
        return redirect('/')
    if request.method == 'POST':
        userName = request.POST.get('userName')
        phoneNo = request.POST.get('phoneNo')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if GUser.username_exists(userName):
            messages.info(request, "Username Taken!!!")
            return redirect('Guser:Signup')
        elif GUser.email_exists(email):
            messages.info(request, "Email Exist!!!")
            return redirect('Guser:Signup')
        else:
            user=GUser.create_user(userName,password,email)
            guser=GUser.create_Guser(user=user,phoneNo=phoneNo)
            login(request, user)
            return redirect(guser)




    return render(request,'signup.html')



@csrf_protect
@login_required
def Active(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if GUser.check_otp(request.user,otp):
            return redirect('/')
        else:
            messages.info(request, "Invalid OTP")
            return redirect(GUser.check_user(request.user))

    return render(request,'active.html')