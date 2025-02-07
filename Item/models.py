from django.core.mail import EmailMessage
from django.db import models
from django.db.models import Subquery
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
import string
import random
from ckeditor.fields import RichTextField
from autoslug import AutoSlugField
from autoslug.settings import slugify

from GrowexoAuction import settings


# from Guser.models import GUser
def custom_slugify(value):
    return slugify(value).replace(' ', '_')

# Create your models here.
class Category(models.Model):
    category_name=models.CharField(max_length=50)
    description=models.TextField(max_length=250,blank=True)
    image=models.ImageField(upload_to='categories_image/',blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-created_at']
    def __str__(self):
        return self.category_name



class Item(models.Model):
    STATUS = (
        ('Active', 'Active'),
        ('UpComing', 'UpComing'),
        ('Under Review', 'Under Review'),
        ('Reject', 'Reject'),
        ('Conditional', 'Conditional'),
        ('Completed', 'Completed'),
    )
    G_user=models.ForeignKey('Guser.GUser', on_delete=models.CASCADE,related_name="user_item")
    slug = AutoSlugField(populate_from='productName',
                         unique_with=['productName'],null=True,
                         slugify=custom_slugify)
    bid_user = models.ManyToManyField('Guser.GUser',through='bid_item')
    productName = models.CharField(max_length=400)
    description = RichTextField(null=True, blank=True)
    base_price = models.BigIntegerField()
    buying_price = models.BigIntegerField()
    status = models.CharField(max_length=20, choices=STATUS, default='Under Review')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now,null=True)

    class Meta:
        ordering=['-created_date']

    def __str__(self):
        return self.productName
    def get_image(self):
        gallery=item_gallery.objects.filter(item=self).first()
        return gallery.image
    def get_images(self):

        return item_gallery.objects.filter(item=self)
    def get_active_item(self):

        return Item.objects.all().filter(status='Active')[:3]

    def get_bid_user(self):

        return bid_item.objects.filter(item=self).order_by('-bid_price')

    def get_bid_higest(self):
        return bid_item.objects.filter(item=self).order_by('-bid_price').first()

    def save_item(request,user):
        c=Category.objects.get(category_name=request.POST.get('category'))
        item=Item.objects.create(G_user=user,productName=request.POST.get('title'),
                                 category=c,description=request.POST.get('description'),
                                 base_price=request.POST.get('Bprice'),buying_price=request.POST.get('BuPrice'),
                                 end_date=request.POST.get('eDate')
                                 )

        images = request.FILES.getlist('uploads')
        for image in images:
            item_gallery.objects.create(item=item,image=image)
    def get_absolute_url(self):
        return reverse("Auction:auction_details", kwargs={"slug": self.slug})
class bid_item(models.Model):
    STATUS = (
        ('Highest', 'Highest'),
        ('Won', 'Won'),
        ('bid', 'bid'),

    )
    item=models.ForeignKey(Item,on_delete=models.CASCADE,default=None)
    bidUser = models.ForeignKey('Guser.GUser', on_delete=models.CASCADE, default=None)
    bid_price = models.BigIntegerField()
    status = models.CharField(max_length=20, choices=STATUS, default='bid')
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering=['-created_date']
    def __str__(self):
        return self.item.productName


class BidSecurity(models.Model):
    STATUS = (
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    bidUser = models.ForeignKey('Guser.GUser', on_delete=models.DO_NOTHING, default=None)
    security_money = models.FloatField(default=0.0)
    number = models.CharField(max_length=200, default="")
    reference_number = models.CharField(max_length=200,default="")
    status = models.CharField(max_length=20, choices=STATUS, default='Unpaid')

    def __str__(self):
        return f"Security money for {self.item.productName} by {self.bidUser.user.username} {self.status}"

    def get_status(item,user):
        try:
            security = BidSecurity.objects.get(item=item,bidUser=user)
            return security.status
        except BidSecurity.DoesNotExist:
            return "False"

@receiver(post_save,sender=bid_item)
def new_bid(sender,instance,**kwargs):
    if instance.status != "Won":
        current_bid_price = instance.bid_price
        item = instance.item
        subquery = bid_item.objects.filter(item=item).exclude(bidUser=instance.bidUser).filter(bid_price__lt=current_bid_price).values('bidUser').distinct()
        from Guser.models import GUser
        bidders = GUser.objects.filter(id__in=Subquery(subquery)).distinct()
        for bidder in bidders:
            print(bidder.user.username)
            if bidder.user.email:
                mail_subject = "New Bid Alert"
                messsage = render_to_string('bid_mail.html', {
                    'user': bidder.user,
                    'product': item,
                })

                email_from = settings.EMAIL_HOST_USER
                recipient_list = [bidder.user.email, ]
                e_message = EmailMessage(mail_subject, messsage, email_from, recipient_list)
                e_message.content_subtype = 'html'
                e_message.send()
                print("send email successfully")
            else:
                pass
    else:
        print("winner bid mail")
        print(instance.bidUser.user.username)
        mail_subject = "Bid Winner"
        messsage = render_to_string('bid_win_mail.html', {
                'user': instance.bidUser.user,
                'product': instance.item,
            })

        email_from = settings.EMAIL_HOST_USER
        recipient_list = [instance.bidUser.user.email, ]
        e_message = EmailMessage(mail_subject, messsage, email_from, recipient_list)
        e_message.content_subtype = 'html'
        e_message.send()
        print("send winner buyer email successfully")
        mail_subject = "Auction End"
        messsage2 = render_to_string('bid_win_seller_mail.html', {
            'user': instance.item.G_user.user,
            'product': instance.item,
            'winner': instance.bidUser.user,
            'price': instance.bid_price,
        })
        print(instance.item.G_user.user.email)
        recipient_list2 = [instance.item.G_user.user.email, ]
        e_message2 = EmailMessage(mail_subject, messsage2, email_from, recipient_list2)
        e_message2.content_subtype = 'html'
        e_message2.send()
        print("send winner seller email successfully")
class item_gallery(models.Model):
    item=models.ForeignKey(Item,on_delete=models.CASCADE,default=None)
    image=models.ImageField(upload_to='item_image/item_gallery/')
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_date']
    def __str__(self):
        return self.item.productName