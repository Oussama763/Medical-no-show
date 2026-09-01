from django.contrib import admin
from .models import Doctor, Patient, TimeSlot, Appointment
from .models import ModelTrainingHistory


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "specialization")
    search_fields = ("user__first_name", "user__last_name", "specialization")


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "gender", "phone")
    search_fields = ("user__first_name", "user__last_name", "phone")
    list_filter = ("gender",)

    def latest_prediction(self, obj):
        try:
            appt = obj.appointments.order_by('-slot__date').first()
            if appt and appt.predicted_no_show is not None:
                return f"{appt.predicted_no_show:.2f}"
        except Exception:
            pass
        return "-"

    latest_prediction.short_description = "Latest no-show"
    list_display = ("id", "user", "gender", "phone", "latest_prediction")


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ("doctor", "date", "start_time", "end_time")
    list_filter = ("date", "doctor")
    ordering = ("date", "start_time")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "slot",
        "status",
        "predicted_no_show",
    )

    list_filter = (
        "status",
        "slot__doctor",
    )

    search_fields = (
        "patient__user__first_name",
        "patient__user__last_name",
        "slot__doctor__user__first_name",
        "slot__doctor__user__last_name",
    )


@admin.register(ModelTrainingHistory)
class ModelTrainingHistoryAdmin(admin.ModelAdmin):
    list_display = ("run_at", "model_name", "accuracy", "data_until")
    readonly_fields = ("run_at", "model_name", "accuracy", "details", "data_until")