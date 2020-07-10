from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime

from .forms import *
from .models import *

categoriesDict = {
    "FA": "Fashion",
    'FO': 'Food',
    'BO': 'Books',
    'TO': 'Toys',
    'EL': 'Electronics',
    'HG': 'Home & Garden',
    'SG': "Sporting Goods",
    'OT': 'Other'
}

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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
            userForm = userForm.save(commit=False)
            userForm.createdUser    = request.user
            userForm.createdDate    = datetime.now()
            userForm.status         = "Active"
            userForm.save()
            return redirect('listing', pk=userForm.pk)
    else:
        userForm = ListingForm()

    return render(request, "auctions/newlisting.html", {
        "listingForm": ListingForm()
    })

def categories(request):
    categoryNames = categoriesDict.values()
    return render(request, "auctions/categories.html", {
        "categories": categoryNames
    })

def getDictKey(category):
    for key, value in categoriesDict.items():
        if category == value:
            return key

def categories_detail(request, category):
    categoryType = getDictKey(category)
    return render(request, "auctions/categories_detail.html", {
        "listings": Listing.objects.all(),
        "category": category,
        "categoryType": categoryType
    })


@login_required
def watchlist(request):
    loggedInUser = request.user
    if request.method == "POST":
        listingID = request.POST.get("listing.id")
        currentListing = Listing.objects.get(id=int(listingID))
        alreadyExists = Watchlist.objects.filter(username=loggedInUser, listing=currentListing)
        
        if not alreadyExists:
            saveWatchlist = Watchlist.objects.create()
            saveWatchlist.username = loggedInUser
            saveWatchlist.listing = currentListing
            saveWatchlist.save()
        
    filteredWatchlist = list(Watchlist.objects.filter(username=loggedInUser))
    userWatchlist = []
    for watchlist in filteredWatchlist:
        userWatchlist.append(watchlist.listing)

    return render(request, "auctions/watchlist.html", {
        "userWatchlist": userWatchlist
    })
    


def listing(request, pk):    
    listing = Listing.objects.get(id=pk) 
    return render(request, "auctions/listing.html", {
        "listing"       : listing,
        "createdUser"   : listing.createdUser,
        "datetime"      : listing.createdDate
    })


