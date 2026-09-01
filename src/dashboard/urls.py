from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.redirect_dashboard, name="redirect"),
    path("admin/", views.admin_dashboard, name="admin"),
    path("doctor/", views.doctor_dashboard, name="doctor"),
    path("doctor/day/<str:date>/", views.doctor_day, name="doctor_day"),
    path("doctor/appointment/<int:pk>/predict/", views.predict_appointment_view, name="predict_appointment"),
    path("doctor/patient/<int:pk>/", views.doctor_patient_detail, name="doctor_patient_detail"),
    path("patient/", views.patient_dashboard, name="patient"),
    path("patient/appointments/", views.patient_appointments, name="patient_appointments"),
    path("patient/appointments/<int:pk>/status/", views.update_appointment_status, name="update_appointment_status"),
    path("patient/book/", views.booking_calendar, name="booking_calendar"),
    path("patient/book/<str:selected_date>/", views.book_appointment, name="book_appointment"),
    path("admin/doctors/", views.doctor_list, name="doctor_list"),
    path("admin/doctors/add/", views.doctor_create, name="doctor_create"),
    path("admin/doctors/<int:pk>/edit/", views.doctor_update, name="doctor_update"),
    path("admin/doctors/<int:pk>/delete/", views.doctor_delete, name="doctor_delete"),
    path("admin/slots/", views.slot_list, name="slot_list"),
    path("admin/slots/generate/", views.generate_slots, name="generate_slots"),
    path("admin/slots/<int:pk>/edit/", views.slot_update, name="slot_update"),
    path("admin/slots/<int:pk>/delete/", views.slot_delete, name="slot_delete"),
    path("admin/patients/", views.admin_patients, name="admin_patients"),
    path("admin/analytics/", views.admin_analytics, name="admin_analytics"),
]