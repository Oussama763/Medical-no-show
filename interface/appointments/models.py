from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    user = models.OneToOneField(
            User,
            on_delete=models.CASCADE,
            null=True
    )

    specialization = models.CharField(max_length=100)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"



class Patient(models.Model):

    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    birth_date = models.DateField()

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES
    )

    phone = models.CharField(
        max_length=20
    )

    def __str__(self):
        return self.user.username



class TimeSlot(models.Model):

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="slots"
    )

    date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    def __str__(self):
        return (
            f"{self.doctor} "
            f"{self.date} "
            f"{self.start_time}"
        )



class Appointment(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
        ("NO_SHOW", "No Show"),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    slot = models.OneToOneField(
        TimeSlot,
        on_delete=models.CASCADE
    )

    booking_date = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    predicted_no_show = models.FloatField(
        null=True,
        blank=True
    )

    def __str__(self):
        return (
            f"{self.patient} - {self.slot}"
        )