from email import message
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django import forms

from .models import User, Auction, Category


def index(request):
    auctions = Auction.objects.all()
    return render(request, "auctions/index.html", {
        'auctions': auctions
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


def create(request):
    if request.method == 'POST':
        newListingForm = CreateListingForm(request.POST)
        if newListingForm.is_valid():
            title = newListingForm.cleaned_data['title']
            description = newListingForm.cleaned_data['description']
            startingBid = newListingForm.cleaned_data['startingBid']
            imageURL = newListingForm.cleaned_data['imageURL']
            category = Category(title=newListingForm.cleaned_data['category'])
            category.save()
            listing = Auction(title=title, description=description, startingBid=startingBid, imageURL=imageURL, category=category, lister=request.user)
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


def auction(request):
     
    
    pass

def watchlist():
    pass
