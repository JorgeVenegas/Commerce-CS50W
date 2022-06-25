from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django import forms
from django.core.exceptions import ObjectDoesNotExist

from auctions.decorators import user_is_auction_author
from django.contrib.auth.decorators import login_required

from .models import Comment, User, Auction, Category, Bid, WatchlistEntry

# FORMS


class CreateListingForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Title'}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Description'}))
    startingBid = forms.DecimalField(widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Starting Bid'}))
    imageURL = forms.URLField(widget=forms.URLInput(
        attrs={'class': 'form-control', 'placeholder': 'Image URL'}))
    category = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Category'}))


class PlaceBidForm(forms.Form):
    amount = forms.DecimalField(widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Bid Amount'}))


class PlaceCommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Comment here...', 'rows': 3}))

# VIEWS


def index(request):
    auctions = Auction.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        'auctions': auctions,
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
            request.session['itemsInWatchList'] = request.user.userWatchlistsEntries.all(
            ).count()
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
            return render(request, "auctions/error.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create(request):
    if request.method == 'POST':
        newListingForm = CreateListingForm(request.POST)
        if newListingForm.is_valid():
            title = newListingForm.cleaned_data['title']
            description = newListingForm.cleaned_data['description']
            startingBid = newListingForm.cleaned_data['startingBid']
            imageURL = newListingForm.cleaned_data['imageURL']
            category, created = Category.objects.get_or_create(
                title=newListingForm.cleaned_data['category'])
            listing = Auction(title=title, description=description, startingBid=startingBid,
                              imageURL=imageURL, category=category, lister=request.user)
            listing.save()

            return redirect('auctions:index')
        else:
            return render(request, "auctions/error.html", {
                'message': "Form is not valid. Try again."
            })

    return render(request, "auctions/create.html", {
        'newListingForm': CreateListingForm()
    })
    pass


def auction(request, pk):
    auction = Auction.objects.get(pk=pk)
    permission = auction.lister.pk == request.user.pk
    PlaceBidFormInitial = {
        'amount': auction.auctionBids.get(current=True).amount + 50 if auction.auctionBids.all() else auction.startingBid + 50
    }
    inWachlist = False

    if request.user.is_authenticated and request.user.userWatchlistsEntries.all():
        if request.user.userWatchlistsEntries.filter(auction=auction).exists():
            inWachlist = True

    return render(request, "auctions/auction.html", {
        'auction': auction,
        'currentBid': auction.currentBid,
        'bids': auction.auctionBids.order_by('-amount'),
        'comments': auction.auctionComments.order_by('-datetime'),
        'permission': permission,
        'placeBidForm': PlaceBidForm(initial=PlaceBidFormInitial),
        'placeCommentForm': PlaceCommentForm(),
        'inWachlist': inWachlist})


@user_is_auction_author
def close(request, pk):
    auction = Auction.objects.get(pk=pk)
    if request.method == 'POST':
        currentBid = auction.currentBid
        auct = Auction(pk=pk, active=False, winner=currentBid.bidder)
        auct.save(update_fields=['active', 'winner'])
    return redirect('auctions:auction', pk=pk)


@user_is_auction_author
def edit(request, pk):
    auction = Auction.objects.get(pk=pk)
    currentCategory = auction.category
    if request.method == 'POST':
        newListingForm = CreateListingForm(request.POST)
        if newListingForm.is_valid():
            title = newListingForm.cleaned_data['title']
            description = newListingForm.cleaned_data['description']
            startingBid = newListingForm.cleaned_data['startingBid']
            imageURL = newListingForm.cleaned_data['imageURL']
            category, created = Category.objects.get_or_create(
                title=newListingForm.cleaned_data['category'])
            listing = Auction(pk=pk, title=title, description=description, startingBid=startingBid,
                              imageURL=imageURL, category=category, lister=request.user)
            listing.save()
            print(currentCategory.auctions.all().count())
            if currentCategory.auctions.all().count() == 0:
                currentCategory.delete()

            return redirect('auctions:auction', pk=pk)
    CreateListingFormInitial = {
        'title': auction.title,
        'description': auction.description,
        'imageURL': auction.imageURL,
        'startingBid': auction.startingBid,
        'category': auction.category.title if auction.category else ""
    }
    return render(request, "auctions/edit.html", {
        'auction': auction,
        'newListingForm': CreateListingForm(initial=CreateListingFormInitial),
    })


@login_required
def bid(request, auction_pk):
    auction = Auction.objects.get(pk=auction_pk)
    if auction.lister == request.user:
        return render(request, "auctions/error.html", {
            "message": "Unable to bid on owned listing."
        })
    if request.method == 'POST':
        placeBidForm = PlaceBidForm(request.POST)
        if placeBidForm.is_valid():
            amount = placeBidForm.cleaned_data['amount']
            if auction.auctionBids.filter(current=True).exists():
                if amount > auction.auctionBids.get(current=True).amount:
                    current_pk = auction.auctionBids.get(current=True).pk
                    current_bid = Bid(pk=current_pk, current=False)
                    current_bid.save(update_fields=["current"])
                else:
                    return render(request, "auctions/error.html", {
                        'message': "Bid must be higher than highest current value."
                    })
            if amount > auction.startingBid:
                bid = Bid(amount=amount, auction=auction, bidder=request.user)
                bid.save()
                auct = Auction(pk=auction_pk, currentBid=bid)
                auct.save(update_fields=["currentBid"])
            else:
                return render(request, "auctions/error.html", {
                    'message': "Bid must be higher than highest current value."
                })
    return redirect('auctions:auction', pk=auction_pk)


@login_required
def comment(request, auction_pk):
    auction = Auction.objects.get(pk=auction_pk)
    if request.method == 'POST':
        placeCommentForm = PlaceCommentForm(request.POST)
        if placeCommentForm.is_valid():
            text = placeCommentForm.cleaned_data['text']
            comment = Comment(auction=auction, text=text, author=request.user)
            comment.save()
    return redirect('auctions:auction', pk=auction_pk)


def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        'categories': categories,
    })


def category(request, title):
    if Category.objects.filter(title=title).exists():
        print("Exists")
        category = Category.objects.get(title=title)
        activeAuctions = Auction.objects.filter(active=True, category=category)
        closedAuctions = Auction.objects.filter(
            active=False, category=category)
    return render(request, "auctions/category.html", {
        'category': category.title,
        'activeAuctions': activeAuctions,
        'closedAuctions': closedAuctions,
    })


@login_required
def edit_watchlist(request, action, auction_pk):
    auction = Auction.objects.get(pk=auction_pk)
    if request.method == 'POST':
        if action == 'add':
            entry = WatchlistEntry(user=request.user, auction=auction)
            entry.save()
        elif action == 'remove':
            entry = WatchlistEntry.objects.filter(
                user=request.user, auction=auction_pk).delete()
    request.session['itemsInWatchList'] = WatchlistEntry.objects.all().count()
    print("Items=" + str(request.session['itemsInWatchList']))
    return redirect('auctions:auction', pk=auction_pk)


@login_required
def watchlist(request):
    try:
        WatchlistsEntries = request.user.userWatchlistsEntries.all()
        print(WatchlistsEntries)
    except ObjectDoesNotExist:
        WatchlistsEntries = None
    return render(request, "auctions/watchlist.html", {
        'WatchlistsEntries': WatchlistsEntries,
    })
