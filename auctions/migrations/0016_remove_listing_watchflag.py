# Generated by Django 3.0.7 on 2020-07-10 04:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_listing_watchflag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='watchFlag',
        ),
    ]
