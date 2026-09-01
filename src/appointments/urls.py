from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("next", views.index_next, name="index_next"),
    #path("", views.index, name="index"),
    #path("", views.index, name="index")
]