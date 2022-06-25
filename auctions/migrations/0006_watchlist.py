# Generated by Django 4.0.5 on 2022-06-25 03:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auction_currentbid_alter_auction_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auction', models.ManyToManyField(related_name='auctionWatchlist', to='auctions.auction')),
                ('user', models.ManyToManyField(related_name='userWatchlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]