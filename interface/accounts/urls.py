from django.urls import path

from . import views

app_name = "accounts"         #added the app_name not to confuse urls

urlpatterns = [
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
]