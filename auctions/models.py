from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    listingID = models.IntegerField()
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    currentBid = models.DecimalField(decimal_places=2, max_digits=15, null=True)
    imageURL = models.URLField(blank=True)
    category = models.CharField(max_length=20)
    status = models.CharField(max_length=10)
    createUser = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    createdDate = models.DateTimeField()

class Bid(models.Model):
    userBid = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listingID = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
    bidAmount = models.DecimalField(decimal_places=2, max_digits=15)


class Comment(models.Model):
    userBid = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listingID = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=200)
    date = models.DateTimeField()

class Watchlist(models.Model):
    userBid = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listingID = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
