# Generated by Django 3.0.7 on 2020-07-09 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_remove_listing_listingid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='createdDate',
            field=models.DateTimeField(null=True),
        ),
    ]