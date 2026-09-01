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
def test_create_doctor():

    user = User.objects.create_user(
        username="doctor1",
        password="password",
        first_name="Ahmed",
        last_name="Alaoui",
    )

    doctor = Doctor.objects.create(
        user=user,
        specialization="Cardiology",
    )

    assert doctor.user.username == "doctor1"
    assert doctor.specialization == "Cardiology"


@pytest.mark.django_db
def test_create_patient():

    user = User.objects.create_user(
        username="patient1",
        password="password",
    )

    patient = Patient.objects.create(
        user=user,
        birth_date=date(2004, 5, 12),
        gender="M",
        phone="0612345678",
    )

    assert patient.user.username == "patient1"
    assert patient.gender == "M"


@pytest.mark.django_db
def test_create_slot():

    doctor_user = User.objects.create_user(
        username="doctor",
        password="password",
    )

    doctor = Doctor.objects.create(
        user=doctor_user,
        specialization="Neurology",
    )

    slot = TimeSlot.objects.create(
        doctor=doctor,
        date=date.today(),
        start_time=time(9, 0),
        end_time=time(9, 30),
    )

    assert slot.doctor == doctor


@pytest.mark.django_db
def test_create_appointment():

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
        phone="0600000000",
    )

    slot = TimeSlot.objects.create(
        doctor=doctor,
        date=date.today(),
        start_time=time(10, 0),
        end_time=time(10, 30),
    )

    appointment = Appointment.objects.create(
        patient=patient,
        slot=slot,
    )

    assert appointment.status == "PENDING"