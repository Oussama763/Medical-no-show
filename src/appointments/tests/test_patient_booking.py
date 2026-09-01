from datetime import date, time

import pytest
from django.contrib.auth.models import User

from appointments.models import Appointment, Doctor, Patient, TimeSlot


@pytest.mark.django_db
def test_patient_can_book_available_slot(client):
    doctor_user = User.objects.create_user(username="doctor", password="password")
    patient_user = User.objects.create_user(username="patient", password="password")

    doctor = Doctor.objects.create(user=doctor_user, specialization="Cardiology")
    patient = Patient.objects.create(
        user=patient_user,
        birth_date=date(1998, 5, 5),
        gender="F",
        phone="0600000000",
    )
    slot = TimeSlot.objects.create(
        doctor=doctor,
        date=date(2030, 1, 15),
        start_time=time(9, 0),
        end_time=time(9, 30),
        is_available=True,
    )

    client.force_login(patient_user)
    response = client.post(f"/dashboard/patient/book/{slot.date.isoformat()}/", {"slot": slot.pk})

    assert response.status_code == 302
    assert Appointment.objects.filter(patient=patient, slot=slot).exists()

    slot.refresh_from_db()
    assert slot.is_available is False


@pytest.mark.django_db
def test_appointment_records_attendance_outcome():
    doctor_user = User.objects.create_user(username="doctor", password="password")
    patient_user = User.objects.create_user(username="patient", password="password")

    doctor = Doctor.objects.create(user=doctor_user, specialization="Cardiology")
    patient = Patient.objects.create(
        user=patient_user,
        birth_date=date(1999, 9, 9),
        gender="M",
        phone="0611111111",
    )
    slot = TimeSlot.objects.create(
        doctor=doctor,
        date=date(2030, 2, 1),
        start_time=time(11, 0),
        end_time=time(11, 30),
    )

    appointment = Appointment.objects.create(patient=patient, slot=slot)

    appointment.record_attendance("SHOWED_UP")
    assert appointment.status == "COMPLETED"

    appointment.record_attendance("NO_SHOW")
    assert appointment.status == "NO_SHOW"
