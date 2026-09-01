from datetime import date, time

import pytest
from django.contrib.auth.models import User

from appointments.models import (
    Doctor,
    Patient,
    TimeSlot,
    Appointment,
)


@pytest.mark.django_db
def test_patient_has_appointments():

    doctor_user = User.objects.create_user(
        username="doctor",
        password="password",
    )

    patient_user = User.objects.create_user(
        username="patient",
        password="password",
    )

    doctor = Doctor.objects.create(
        user=doctor_user,
        specialization="Cardiology",
    )

    patient = Patient.objects.create(
        user=patient_user,
        birth_date=date(2000, 1, 1),
        gender="M",
        phone="0611111111",
    )

    slot = TimeSlot.objects.create(
        doctor=doctor,
        date=date.today(),
        start_time=time(9, 0),
        end_time=time(9, 30),
    )

    Appointment.objects.create(
        patient=patient,
        slot=slot,
    )

    assert patient.appointments.count() == 1


@pytest.mark.django_db
def test_doctor_has_slots():

    doctor_user = User.objects.create_user(
        username="doctor",
        password="password",
    )

    doctor = Doctor.objects.create(
        user=doctor_user,
        specialization="Cardiology",
    )

    TimeSlot.objects.create(
        doctor=doctor,
        date=date.today(),
        start_time=time(9, 0),
        end_time=time(9, 30),
    )

    assert doctor.slots.count() == 1