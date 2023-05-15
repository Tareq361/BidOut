from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.http import urlencode
from django.utils import timezone
from Guser.models import GUser
from Item.models import *


# Create your views here.
def Home(request):
    context = {}
    if request.user.is_authenticated:
        context['guser'] = GUser.check_user(request.user)
    items = Item.get_active_item(request);
    context['items'] = items
    return render(request, "home.html", context)


def item_completed(request):
    if request.method == "POST":
        print("success item")
        item_id = request.POST.get('item_id')
        item = Item.objects.get(id=item_id)
        if item.end_date <= timezone.now() and item.status != 'Completed':
            print(item)
            item.status = 'Completed'
            item.save()

            # Notify the highest bidder
            if item.bid_user.count() > 0:
                # highest_bidder = item.bid_user.order_by('-bid_item__bid_price').first()
                # send notification using channels or other way
                higest_price = item.get_bid_higest()
                higest_price.status = "Won"
                higest_price.save()
                # print(highest_bidder)
                # print(
                #     f'Item {item.id} has ended. {highest_bidder.user.username} won the auction for {item.productName} with a bid of {higest_price.bid_price}.')
                # print("winner bid mail")
                #
                # mail_subject = "Bid Winner"
                # messsage1 = render_to_string('bid_win_mail.html', {
                #     'user': highest_bidder.user,
                #     'product': item,
                # })
                #
                # email_from = settings.EMAIL_HOST_USER
                # recipient_list = [highest_bidder.user.email, ]
                # e_message = EmailMessage(mail_subject, messsage1, email_from, recipient_list)
                # e_message.content_subtype = 'html'
                # e_message.send()
                # print("send winner buyer email successfully")
                # mail_subject = "Auction End"
                # messsage2 = render_to_string('bid_win_seller_mail.html', {
                #     'user': item.G_user.user,
                #     'product': item,
                #     'winner':highest_bidder.user,
                #     'price':higest_price.bid_price,
                # })
                # recipient_list2 = [item.G_user.user.email, ]
                # e_message2 = EmailMessage(mail_subject, messsage2, email_from, recipient_list2)
                # e_message2.content_subtype = 'html'
                # e_message2.send()
                # print("send winner seller email successfully")
            else:
                # Notify the seller that there were no bids
                # send notification using channels or other way
                print(f'Item {item.id} has ended. There were no bids for {item.productName}.')
            return HttpResponse("ok")
        else:
            return HttpResponse("completed already", status=400)


def Login(request):
    if request.user.is_authenticated:
        print("true")

        return redirect('/')
    else:

        if request.method == "POST":
            print("success")
            userName = request.POST.get('user_name')
            pass1 = request.POST.get('password')
            user = authenticate(request, username=userName, password=pass1)
            if user is None:
                print("no user")
                next_param = request.POST.get('next', '')
                print(next_param)
                redirect_url = f"{reverse('Main:Login')}?{urlencode({'next': next_param})}"
                messages.info(request, "User doesn't exist")
                return redirect(redirect_url)

                # if GUser.user_exist(userName,pass1):
                #     user=GUser.get_user(userName,pass1)
                #
                # else:
                #     messages.info(request, "Password doesn't match")
                #     return redirect('Main:Login')
            else:
                login(request, user)
                print("user")
                print(request.POST.get('next'))
                if request.POST.get('next'):
                    print("inside next")
                    next_param = request.POST.get('next', '')
                    return redirect(next_param)
                else:
                    return redirect('Main:Home')
        return render(request, "login.html")


@login_required
def Logout(request):
    logout(request);
    return redirect('/')


@login_required
def send_security_money(request):
    if request.method == "POST":
        item = Item.objects.get(id=request.POST.get('item_id'))
        BidSecurity.objects.create(item=item, bidUser=request.user.guser_user, security_money=item.base_price*0.10,
                                   number=request.POST.get('number'), reference_number=f"{item.id}{request.user.guser_user.id}")

        return HttpResponse("ok", status=200)
