from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="/accounts/login/"),
        name="logout",
    ),
    path("register/", views.register, name="register"),
    path("verify/<str:username>/", views.verify_email, name="verify_email"),
    path("verify/<str:username>/resend/", views.resend_code, name="resend_code"),
    path("dashboard/", views.dashboard, name="dashboard"),
]