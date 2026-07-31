from django.urls import path
import sys
sys.path.append("appointments")
from appointments import views

urlpatterns = [
    path("", views.index, name="index")
    #path("", views.index, name="index"),
    #path("", views.index, name="index"),
    #path("", views.index, name="index")
]