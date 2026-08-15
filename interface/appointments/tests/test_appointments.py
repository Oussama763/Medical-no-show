from datetime import date, time

import pytest
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from appointments.models import (
    Doctor,
    Patient,
    TimeSlot,
    Appointment,
)


@pytest.mark.django_db
def test_one_slot_one_appointment():

    doctor_user = User.objects.create_user(
        username="doctor",
        password="password",
    )

    patient1_user = User.objects.create_user(
        username="patient1",
        password="password",
    )

    patient2_user = User.objects.create_user(
        username="patient2",
        password="password",
    )

    doctor = Doctor.objects.create(
        user=doctor_user,
        specialization="Cardiology",
    )

    patient1 = Patient.objects.create(
        user=patient1_user,
        birth_date=date(2000, 1, 1),
        gender="M",
        phone="0600",
    )

    patient2 = Patient.objects.create(
        user=patient2_user,
        birth_date=date(2000, 1, 1),
        gender="F",
        phone="0700",
    )

    slot = TimeSlot.objects.create(
        doctor=doctor,
        date=date.today(),
        start_time=time(9, 0),
        end_time=time(9, 30),
    )

    Appointment.objects.create(
        patient=patient1,
        slot=slot,
    )

    with pytest.raises(IntegrityError):
        Appointment.objects.create(
            patient=patient2,
            slot=slot,
        )