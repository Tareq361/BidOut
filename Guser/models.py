from autoslug import AutoSlugField
from autoslug.settings import slugify
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from Item.models import Item


def custom_slugify(value):
    return slugify(value).replace(' ', '_')
class GUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
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
    def phoneNo_exists(pno):
        if GUser.objects.filter(phoneNumber=pno).exists():
            return True

        return False
    def check_otp(slug,otp):
        if GUser.objects.filter(slug=slug,otp=otp).exists():
            gu=GUser.objects.get(slug=slug,otp=otp);
            gu.otp_active=True
            gu.save()
            return True
        return False
    def create_user(userName,password):
        user=User.objects.create_user(username=userName, password=password)

        return user
    def check_user(user):
        user=GUser.objects.get(user=user)

        return user
    def create_Guser(user, phoneNo):
        guser = GUser.objects.create(user=user, otp='1234', phoneNumber=phoneNo)

        return guser
    def get_own_item(self):

        return Item.objects.filter(G_user=self)
    def get_absolute_url(self):
        return reverse("Guser:Active", kwargs={"slug": self.slug})

    def get_absolute_url_dashboard(self):
        return reverse("dashboard:mydashboard", kwargs={"slug": self.slug})