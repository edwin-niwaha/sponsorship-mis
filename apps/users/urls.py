from django.urls import path

from .views import RegisterView, home, profile, contact_us

urlpatterns = [
    path("", home, name="users-home"),
    path("register/", RegisterView.as_view(), name="users-register"),
    path("profile/", profile, name="users-profile"),
    path("contact-us/", contact_us, name="contact_us"),]
