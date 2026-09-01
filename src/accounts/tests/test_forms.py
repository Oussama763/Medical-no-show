import pytest

from django.contrib.auth.models import User

from accounts.forms import PatientRegistrationForm
from appointments.models import Patient


@pytest.mark.django_db
def test_registration_form_creates_user_and_patient():

    form = PatientRegistrationForm(data={
        "username": "oussama",
        "first_name": "Oussama",
        "last_name": "Pro",
        "email": "oussama@test.com",
        "birth_date": "2004-05-12",
        "gender": "M",
        "phone": "0612345678",
        "password1": "StrongPassword123",
        "password2": "StrongPassword123",
    })

    assert form.is_valid()

    user = form.save()

    assert User.objects.count() == 1
    assert Patient.objects.count() == 1

    patient = Patient.objects.first()

    assert patient.user == user
    assert patient.phone == "0612345678"


@pytest.mark.django_db
def test_passwords_must_match():

    form = PatientRegistrationForm(data={
        "username": "oussama",
        "first_name": "Oussama",
        "last_name": "Pro",
        "email": "oussama@test.com",
        "birth_date": "2004-05-12",
        "gender": "M",
        "phone": "0612345678",
        "password1": "Password123",
        "password2": "AnotherPassword",
    })

    assert not form.is_valid()