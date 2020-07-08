# Generated by Django 3.0.7 on 2020-07-08 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20200708_0251'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='startingBid',
            new_name='currentBid',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='image',
        ),
        migrations.AddField(
            model_name='listing',
            name='imageURL',
            field=models.URLField(blank=True),
        ),
    ]
