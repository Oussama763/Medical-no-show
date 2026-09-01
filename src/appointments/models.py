from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    user = models.OneToOneField(
            User,
            on_delete=models.CASCADE,
            null=True,
            blank=True,
    )

    specialization = models.CharField(max_length=100)

    appointment_duration = models.PositiveIntegerField(
        default=30,
        help_text="Default appointment duration in minutes."
    )

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["specialization"]),
        ]

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

    # Location for future ML features
    city = models.CharField(max_length=100, blank=True, null=True)
    neighborhood = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["gender"]),
        ]

    def __str__(self):
        return self.user.username

    # Additional clinical flags to record patient conditions
    diabetes = models.BooleanField(default=False)
    hypertension = models.BooleanField(default=False)
    handicapped = models.BooleanField(default=False)

    # Email verification fields: store a 6-digit code and verification state
    email_verified = models.BooleanField(default=False)
    email_verification_code = models.CharField(max_length=6, null=True, blank=True)





class TimeSlot(models.Model):

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="slots"
    )

    date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    is_available = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=["doctor", "date", "is_available"]),
            models.Index(fields=["date", "is_available", "start_time"]),
        ]

    def __str__(self):
        return (
            f"{self.doctor}"
            f"{self.date}"
            f"{self.start_time}-{self.end_time}"
        )



class Appointment(models.Model):

    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    NO_SHOW = "NO_SHOW"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (CONFIRMED, "Confirmed"),
        (COMPLETED, "Completed"),
        (CANCELLED, "Cancelled"),
        (NO_SHOW, "No Show"),
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
        default=PENDING
    )

    predicted_no_show = models.FloatField(
        null=True,
        blank=True
    )

    class Meta:
        indexes = [
            models.Index(fields=["patient", "status"]),
            models.Index(fields=["status", "booking_date"]),
            models.Index(fields=["slot", "status"]),
        ]

    @property
    def attended(self):
        return self.status in {self.COMPLETED, self.CONFIRMED}

    @property
    def missed(self):
        return self.status == self.NO_SHOW

    def record_attendance(self, outcome):
        normalized = (outcome or "").strip().upper().replace(" ", "_")

        if normalized in {"SHOWED_UP", "ATTENDED", "COMPLETED"}:
            self.status = self.COMPLETED
        elif normalized in {"NO_SHOW", "MISSED", "MISSED_APPOINTMENT"}:
            self.status = self.NO_SHOW
        elif normalized == "CANCELLED":
            self.status = self.CANCELLED
        elif normalized in {"CONFIRMED", "BOOKED"}:
            self.status = self.CONFIRMED
        else:
            self.status = self.PENDING

        self.save(update_fields=["status"])

        if self.slot_id:
            self.slot.is_available = self.status not in {self.CANCELLED, self.COMPLETED, self.NO_SHOW}
            self.slot.save(update_fields=["is_available"])

    def __str__(self):
        return (
            f"{self.patient} - {self.slot}"
        )



class ModelTrainingHistory(models.Model):
    """Record of model training runs and their evaluation metrics."""
    run_at = models.DateTimeField(auto_now_add=True)
    model_name = models.CharField(max_length=100)
    accuracy = models.FloatField(null=True, blank=True)
    details = models.JSONField(null=True, blank=True)
    # Data until this timestamp (appointments included up to this booking_date)
    data_until = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-run_at",)

    def __str__(self):
        return f"{self.run_at.isoformat()} - {self.model_name} ({self.accuracy})"