from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.categories_detail, name="categories_detail"),
    path("newlisting", views.newlisting, name="newlisting"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("closedlistings", views.closedListing, name="closedlistings"),
    path(r"listing/<int:pk>", views.listing, name="listing")
]
