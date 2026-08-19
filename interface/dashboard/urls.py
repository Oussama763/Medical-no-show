from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.redirect_dashboard, name="redirect"),
    path("admin/", views.admin_dashboard, name="admin"),
    path("doctor/", views.doctor_dashboard, name="doctor"),
    path("patient/", views.patient_dashboard, name="patient"),
]