# Generated by Django 4.0.5 on 2022-06-25 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_rename_auction_watchlist_auctions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchlist',
            old_name='auctions',
            new_name='auction',
        ),
    ]
