from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    title = models.CharField(unique=True, max_length=25)

    def __str__(self) -> str:
        return f'Category: {self.title}'


class Auction(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=120)
    startingBid = models.DecimalField(max_digits=9, decimal_places=2)
    imageURL = models.URLField()
    category = models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL, related_name="auctions")
    lister = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings")
    currentBid = models.OneToOneField(
        'Bid', on_delete=models.SET_NULL, null=True, related_name='currentBidAuction')
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="winninglistings")

    def __str__(self) -> str:
        return f'Auction: {self.title} by {self.lister}.'


class Bid(models.Model):
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="auctionBids")
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="userBids")
    datetime = models.DateTimeField(auto_now=True)
    current = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.bidder}\'s bid for ${self.amount} for {self.auction}. '


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="userComments")
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="auctionComments")
    text = models.CharField(max_length=300)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'Coment by {self.author}: "{self.text}"'


class WatchlistEntry(models.Model):
    user = models.ForeignKey(
        User, default=None, on_delete=models.CASCADE, related_name="userWatchlistsEntries")
    auction = models.ForeignKey(
        Auction, default=None, on_delete=models.CASCADE, related_name="auctionWatchlist")

    def __str__(self) -> str:
        return f'Watchlist entry of {self.user.username} on "{self.auction.title}"'
