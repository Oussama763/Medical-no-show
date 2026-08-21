from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.redirect_dashboard, name="redirect"),
    path("admin/", views.admin_dashboard, name="admin"),
    path("doctor/", views.doctor_dashboard, name="doctor"),
    path("patient/", views.patient_dashboard, name="patient"),
    path("admin/doctors/", views.doctor_list, name="doctor_list"),
    path("admin/doctors/add/", views.doctor_create, name="doctor_create"),
    path("admin/doctors/<int:pk>/edit/", views.doctor_update, name="doctor_update"),
    path("admin/doctors/<int:pk>/delete/", views.doctor_delete, name="doctor_delete"),
]