"""URL routes for account-related views."""

from django.urls import path

from .views import SalonLoginView, SalonLogoutView, logout_redirect, profile, register

app_name = "accounts"


urlpatterns = [
    path("login/", SalonLoginView.as_view(), name="login"),
    path("logout/", logout_redirect, name="logout"),
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),
]