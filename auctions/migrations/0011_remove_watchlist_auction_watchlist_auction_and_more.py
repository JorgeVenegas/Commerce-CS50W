# Generated by Django 4.0.5 on 2022-06-25 06:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_remove_watchlist_auction_watchlist_auction_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='auction',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='auction',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='auctionWatchlist', to='auctions.auction'),
        ),
        migrations.RemoveField(
            model_name='watchlist',
            name='user',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='userWatchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
