# Generated by Django 3.0.7 on 2020-07-09 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20200709_0218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, choices=[('FA', 'Fashion'), ('BO', 'Books'), ('TO', 'Toys'), ('EL', 'Electronics'), ('HG', 'Home & Garden'), ('SG', 'Sporting Goods'), ('OT', 'Other')], max_length=20),
        ),
    ]