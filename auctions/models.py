from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm


class User(AbstractUser):
    pass

class Listing(models.Model):
    title       = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    currentBid  = models.DecimalField(decimal_places=2, max_digits=15, null=True)
    imageURL    = models.URLField(blank=True)
    status      = models.CharField(max_length=1, null=True)
    createdUser = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    createdDate = models.DateTimeField(null=True)

    CATEGORIES = [
        ('FA', 'Fashion'),
        ('FO', 'Food'),
        ('BO', 'Books'),
        ('TO', 'Toys'),
        ('EL', 'Electronics'),
        ('HG', 'Home & Garden'),
        ('SG', "Sporting Goods"),
        ('OT', 'Other')
    ]

    category = models.CharField(max_length=20, choices=CATEGORIES, blank=True)


class Bid(models.Model):
    username    = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listing     = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
    bidAmount   = models.DecimalField(decimal_places=2, max_digits=15)


class Comment(models.Model):
    username    = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listing     = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
    comment     = models.CharField(max_length=200)
    date        = models.DateTimeField()

class Watchlist(models.Model):
    username    = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listing     = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
