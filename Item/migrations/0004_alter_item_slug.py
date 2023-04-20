# Generated by Django 4.1.2 on 2022-12-15 21:39

import Item.models
import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Item', '0003_alter_item_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, null=True, populate_from=['productName', 'start_date'], slugify=Item.models.custom_slugify, unique_with=['productName']),
        ),
    ]
