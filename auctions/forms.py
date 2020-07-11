from django.forms import ModelForm
from django.db import models
from .models import *

class ListingForm(ModelForm):
    class Meta:
        model   = Listing
        fields  = ['title', 'description', 'initialBid', 'category', 'imageURL']
        labels  = {
            "title": "Title",
            "description": "Description",
            "initialBid": "Starting Bid (in USD)",
            "category": "Category",
            "imageURL": "Image URL"
            }

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bidAmount']
        labels = {
            "bidAmount": ""
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        labels = {
            "comment": ""
        }