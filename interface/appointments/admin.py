from django.contrib import admin
from .models import Doctor, Patient, TimeSlot, Appointment

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(TimeSlot)
admin.site.register(Appointment)