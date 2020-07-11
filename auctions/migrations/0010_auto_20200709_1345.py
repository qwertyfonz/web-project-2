# Generated by Django 3.0.7 on 2020-07-09 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20200709_0349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, choices=[('FA', 'Fashion'), ('FO', 'Food'), ('BO', 'Books'), ('TO', 'Toys'), ('EL', 'Electronics'), ('HG', 'Home & Garden'), ('SG', 'Sporting Goods'), ('OT', 'Other')], default='FA', max_length=20),
        ),
    ]
