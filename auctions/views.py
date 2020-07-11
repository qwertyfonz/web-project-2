from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime

from .forms import *
from .models import *

# Categories dictionary
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

# Returns main page of all active listings
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
        username    = request.POST["username"]
        email       = request.POST["email"]

        # Ensure password matches confirmation
        password       = request.POST["password"]
        confirmation   = request.POST["confirmation"]
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

# Creates a new listing
def newlisting(request):
    userForm = ListingForm(request.POST)
    
    # If the request method is POST, save all forms into a new ModelFrom
    if request.method == "POST":
        if userForm.is_valid():
            userForm                = userForm.save(commit=False)
            userForm.createdUser    = request.user
            userForm.createdDate    = datetime.now()
            userForm.status         = "Active"
            userForm.save()
            return redirect('listing', pk=userForm.pk)
    # Else return back the form
    else:
        userForm = ListingForm()

    return render(request, "auctions/newlisting.html", {
        "listingForm": ListingForm()
    })

# Get category names
def categories(request):
    categoryNames = categoriesDict.values()
    return render(request, "auctions/categories.html", {
        "categories": categoryNames
    })

# Get key name from value
def getDictKey(category):
    for key, value in categoriesDict.items():
        if category == value:
            return key

# List all categories
def categories_detail(request, category):
    categoryType = getDictKey(category)
    return render(request, "auctions/categories_detail.html", {
        "listings"      : Listing.objects.all(),
        "category"      : category,
        "categoryType"  : categoryType
    })

# Create a watchlist
@login_required
def watchlist(request):
    loggedInUser = request.user
    if request.method == "POST":
        # Get the current listing
        listingID       = request.POST.get("listing.id")
        currentListing  = Listing.objects.get(id=int(listingID))

        # Check to see if listing is already in watchlist
        alreadyExists   = Watchlist.objects.filter(username=loggedInUser, listing=currentListing)
        
        # If already in watchlist, then pressing button will delete it
        if alreadyExists:
            alreadyExists.delete()

        # If not in watchlist, then create a new Watchlist object and save it
        else:
            saveWatchlist           = Watchlist.objects.create()
            saveWatchlist.username  = loggedInUser
            saveWatchlist.listing   = currentListing
            saveWatchlist.save()

    # Filter for a list of all Watchlist listings    
    filteredWatchlist = list(Watchlist.objects.filter(username=loggedInUser))
    userWatchlist = []
    for watchlist in filteredWatchlist:
        userWatchlist.append(watchlist.listing)

    return render(request, "auctions/watchlist.html", {
        "userWatchlist": userWatchlist
    })

def doesWatchListExist(username, listing):
    return Watchlist.objects.filter(username=username, listing=listing)

def bidding(request, listing, pk, username, args):

    # Checks to see if there are any existing bids on this listing
    checkBidExists  = Bid.objects.filter(listing=pk)

    # Create new bid form object based on user submit
    bidForm         = BidForm(request.POST)
    
    if request.method == "POST" and 'bidvalue' in request.POST:
        if bidForm.is_valid():
            bidForm = bidForm.save(commit=False)

            # If the user-entered values don't conform to given rules (at least equal or higher)
            # Give exceptions
            if not checkBidExists:
                if bidForm.bidAmount < listing.initialBid:
                    args.update({"error1": True})
                    return render(request, "auctions/listing.html", args)
            else:
                if bidForm.bidAmount <= listing.initialBid:
                    args.update({"error2": True})
                    return render(request, "auctions/listing.html", args)
                
            # Save Bidform ModelForm and update Listing's new amount
            bidForm.username    = username
            bidForm.listing     = listing
            bidForm.save()

            listing.initialBid  = bidForm.bidAmount
            listing.save()

            return redirect('listing', pk=listing.pk)

def closedListing(request):

    # If user closes listing, update its status to "Closed"
    if request.method == "POST":
        listingID       = request.POST.get("listing.id")
        listing         = Listing.objects.get(id=listingID)
        listing.status  = "Closed"
        listing.save()

    return render(request, "auctions/closedlistings.html", {
        "listings": Listing.objects.all()
    })

# Create and save new comment
def newComment(request, listing):
    commentForm = CommentForm(request.POST)
    if request.method == "POST" and 'comment' in request.POST:
        if commentForm.is_valid():
            commentForm          = commentForm.save(commit=False)
            commentForm.username = request.user
            commentForm.listing  = listing
            commentForm.date     = datetime.now()
            commentForm.save()
    

# All functions to create a listing page    
def listing(request, pk):   

    # Get listing based on id, bid value based on form input
    listing         = Listing.objects.get(id=pk)
    loggedInUser    = request.user

    # Initialize a watchlist flag to false; to update later if listing is already on user's watchlist
    watchlistFlag   = False

    args = {        "listing"       : listing,
                    "createdUser"   : listing.createdUser,
                    "datetime"      : listing.createdDate,
                    "watchlistFlag" : watchlistFlag,
                    "loggedInUser"  : loggedInUser,
                    "bidForm"       : BidForm(),
                    "commentForm"   : CommentForm()
                }
    
    # Display all comments (if there are any)
    if len(Comment.objects.filter(listing=listing)) != 0:
        allComments = Comment.objects.filter(listing=listing)
        args.update({"allComments": allComments})

    # If listing is closed, find the highest bidder (if there are any)
    if len(Bid.objects.filter(listing=listing)) != 0:
        if listing.status == "Closed": 
            highestBidder = Bid.objects.filter(listing=listing).latest('listing').username
            args.update({"highestBidder": highestBidder})
    
    # If the current user is authenticated
    if loggedInUser.is_authenticated:

        # Checks to see if item is on user's watchlist
        if doesWatchListExist(loggedInUser, listing):
            watchlistFlag = True
            args.update({"watchlistFlag": watchlistFlag})

        # Save highest bid
        bidding(request, listing, pk, loggedInUser, args)

        # Save new comment
        newComment(request, listing)

    return render(request, "auctions/listing.html", args)
