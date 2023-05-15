from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_protect

from GrowexoAuction import settings
from .models import GUser


# Create your views here.
@csrf_protect
def Signup(request):
    phoneNo = ''
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
            user = GUser.create_user(userName, password, email)
            guser = GUser.create_Guser(user=user, phoneNo=phoneNo)
            login(request, user)
            return redirect(guser)

    return render(request, 'signup.html')


@csrf_protect
@login_required
def Active(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if GUser.check_otp(request.user, otp):
            return redirect('/')
        else:
            messages.info(request, "Invalid OTP")
            return redirect(GUser.check_user(request.user))

    return render(request, 'active.html')


@csrf_protect
def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if GUser.email_exists(email):
            messages.info(request, "An email has been send to your mail. Please follow the instruction in email for "
                                   "rest your password")
            user = User.objects.get(email=email)
            # reset password email
            current_site = get_current_site(request)
            mail_subject = "Reset password"
            messsage = render_to_string('reset_password_mail.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail(mail_subject, messsage, email_from, recipient_list)
            print("send reset password link successfully")
        else:
            messages.info(request, "Invalid Email")

    return render(request, 'forget_password.html')
def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        print(uid)
        user = User.objects.get(pk=uid)

    except:
        user = None
        print("failed")

    if user is not None and default_token_generator.check_token(user, token):
        request.session['cid'] = uid
        messages.success(request, "please reset your password")
        return redirect('/reset_password')
    else:
        messages.warning(request, "Link expired!!!")
        return redirect('Main:Login')


def reset_password(request):
    if request.session.get('cid'):
        if request.method == "POST":
            password = request.POST.get("create_password")
            confirm_password = request.POST.get("confirm_password")
            if password == confirm_password:
                cid = request.session.get('cid')
                user = User.objects.get(pk=cid)
                new_pass = make_password(confirm_password)
                user.password = new_pass
                user.save()
                messages.success(request, "Reset password successfully!!!")
                return redirect('/Login')
            else:
                messages.error(request, "Password doesn't match!!!")
                return redirect('/reset_password')
        else:
            return render(request, 'reset_password.html')
    else:
        return redirect('/')