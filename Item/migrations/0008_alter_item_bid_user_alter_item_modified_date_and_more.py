# Generated by Django 4.0 on 2023-04-20 18:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Guser', '0009_alter_guser_slug'),
        ('Item', '0007_alter_item_description_alter_item_productname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='bid_user',
            field=models.ManyToManyField(through='Item.bid_item', to='Guser.GUser'),
        ),
        migrations.AlterField(
            model_name='item',
            name='modified_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.CreateModel(
            name='BidSecurity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('security_money', models.FloatField(default=0.0)),
                ('bidUser', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='Guser.guser')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Item.item')),
            ],
        ),
    ]
