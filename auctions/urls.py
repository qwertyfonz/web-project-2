from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # path("categories", views.categories, name="categories"),
    path("newlisting", views.newlisting, name="newlisting"),
    # path("watchlist", views.watchlist, name="watchlist"),
    path(r"listing/<int:pk>", views.listing, name="listing")
]
