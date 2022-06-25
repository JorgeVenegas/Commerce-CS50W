from django.contrib import admin

# Register your models here.
from .models import Auction, Bid, Category, Comment, WatchlistEntry

admin.site.site_header = 'Commerce Django Dashboard'
admin.site.register(Category)
admin.site.register(Auction)
admin.site.register(Comment)
admin.site.register(WatchlistEntry)
admin.site.register(Bid)
