from django.contrib import admin
from Item import models
# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.Item)
admin.site.register(models.item_gallery)
admin.site.register(models.bid_item)