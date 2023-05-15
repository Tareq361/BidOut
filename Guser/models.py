from autoslug import AutoSlugField
from autoslug.settings import slugify
from django.core.mail import send_mail, EmailMessage
from django.db import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.urls import reverse

from GrowexoAuction import settings
from Item.models import Item, bid_item
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
def custom_slugify(value):
    return slugify(value).replace(' ', '_')
class GUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="guser_user")
    phoneNumber = models.CharField(max_length=14,null=False)
    otp=models.CharField(max_length=4,null=True)
    slug = AutoSlugField(populate_from='phoneNumber',
                         unique_with=['phoneNumber'],null=True,
                         slugify=custom_slugify)
    otp_active=models.BooleanField(default=False,null=True)

    def __str__(self):
        return self.user.username

    def username_exists(username):
        if User.objects.filter(username=username).exists():
            return True

        return False
    def user_exist(userName,password):
        if User.objects.filter(username=userName,password=password).exists():
            return True

        return False
    def get_user(username,password):
        if User.objects.filter(username=username,password=password).exists():
            return User.objects.get(username=username,password=password)

        return False
    def email_exists(email):
        if User.objects.filter(email=email).exists():
            return True

        return False
    def check_otp(user,otp):
        if GUser.objects.filter(user=user,otp=otp).exists():
            gu=GUser.objects.get(user=user,otp=otp);
            gu.otp_active=True
            gu.save()
            return True
        return False
    def create_user(userName,password,email):
        user=User.objects.create_user(username=userName, password=password,email=email)

        return user
    def check_user(user):
        user=GUser.objects.get(user=user)

        return user
    def create_Guser(user, phoneNo):
        guser = GUser.objects.create(user=user, otp=get_random_string(4, allowed_chars='0123456789'), phoneNumber=phoneNo)
        mail_subject = "OTP for account active"
        messsage = render_to_string('otp_mail.html', {
            'user': user,
            'otp': guser.otp,
        })

        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        e_message = EmailMessage(mail_subject, messsage, email_from, recipient_list)
        e_message.content_subtype = 'html'
        e_message.send()
        print("send activation link successfully")
        return guser
    def update_user(request):
        request.user.username=request.POST.get('username')
        if request.POST.get('confirm_password'):
            request.user.set_password(request.POST.get('confirm_password'))
            mail_subject = "Password Changed"
            messsage = render_to_string('password_change.html', {
                'user': request.user,

            })

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.user.email, ]
            e_message = EmailMessage(mail_subject, messsage, email_from, recipient_list)
            e_message.content_subtype = 'html'
            e_message.send()
            print("send email successfully")

        request.user.save()
        return True
    def get_own_item(self):

        return Item.objects.filter(G_user=self)
    def get_bid_item(self):
        bid_items = bid_item.objects.filter(bidUser=self).order_by('item', '-created_date')
        unique_items = {}
        for item in bid_items:
            if item.item not in unique_items:
                unique_items[item.item] = item
        return list(unique_items.values())
    def get_absolute_url(self):
        return reverse("Guser:Active")

# @receiver(post_save,sender=GUser)
# def otp_for_guser(sender,instance,**kwargs):

