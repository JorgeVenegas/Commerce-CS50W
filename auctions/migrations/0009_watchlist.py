# Generated by Django 4.0.5 on 2022-06-25 05:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_delete_watchlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auction', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='auctionWatchlist', to='auctions.auction')),
                ('user', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='userWatchlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]