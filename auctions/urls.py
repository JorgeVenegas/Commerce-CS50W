from django.urls import path

from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("edit/<int:pk>", views.edit, name="edit"),
    path("auction/<int:pk>", views.auction, name="auction"),
    path("close/<int:pk>", views.close, name="close"),
    path("bid/<int:auction_pk>", views.bid, name="bid"),
    path("comment/<int:auction_pk>", views.comment, name="comment"),
    path("categories/<str:title>", views.category, name="category"),
    path("categories", views.categories, name="categories"),
    path("watchlist/<str:action>/<int:auction_pk>",
         views.edit_watchlist, name="edit_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
]
