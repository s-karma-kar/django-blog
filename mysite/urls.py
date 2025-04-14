# mysite/urls.py
from django.contrib import admin
from django.urls import path, include  # <-- Make sure you have both of these imports.
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
    path("polling/", include("polling.urls")),  # <-- Add this
    path("admin/", admin.site.urls),
    path("", include("blogging.urls")),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
]
