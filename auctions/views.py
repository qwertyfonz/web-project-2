from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import ModelForm
from django import forms
from datetime import datetime

from .models import *

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "datetime": datetime.now()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def newlisting(request):
    userForm = ListingForm(request.POST)
    
    if request.method == "POST":
        if userForm.is_valid():
            form = userForm.save(commit=False)
            form.user = User.username
            form.date = datetime.now()
            form.status = "Active"
            form.save()
            return redirect('listing', pk=form.pk)
    else:
        form = ListingForm()

    return render(request, "auctions/newlisting.html", {
        "listingForm": ListingForm()
    })
"""
def categories(request):

def watchlist(request):
"""

def listing(request, pk):
    listing = Listing.objects.get(id=pk)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "user": User.username,
        "datetime": datetime.now()
    })


