# Generated by Django 3.0.7 on 2020-07-08 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20200708_0327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('FA', 'Fashion'), ('BO', 'Books'), ('TO', 'Toys'), ('EL', 'Electronics'), ('HG', 'Home & Garden'), ('SG', 'Sporting Goods'), ('OT', 'Other')], max_length=20),
        ),
    ]
