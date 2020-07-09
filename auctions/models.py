from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    currentBid = models.DecimalField(decimal_places=2, max_digits=15, null=True)
    imageURL = models.URLField(blank=True)
    status = models.CharField(max_length=10)
    createdUser = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    createdDate = models.DateTimeField(null=True)

    CATEGORIES = [
        ('FA', 'Fashion'),
        ('BO', 'Books'),
        ('TO', 'Toys'),
        ('EL', 'Electronics'),
        ('HG', 'Home & Garden'),
        ('SG', "Sporting Goods"),
        ('OT', 'Other')
    ]

    category = models.CharField(max_length=20, choices=CATEGORIES, blank=True)


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'currentBid', 'category', 'imageURL']
        labels = {
            "title": "Title",
            "description": "Description",
            "currentBid": "Starting Bid (in USD)",
            "category": "Category",
            "imageURL": "Image URL"
            }


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
