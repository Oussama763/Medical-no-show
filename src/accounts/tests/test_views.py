import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from appointments.models import Patient


@pytest.mark.django_db
def test_register_page_loads(client):

    response = client.get(reverse("register"))

    assert response.status_code == 200



@pytest.mark.django_db
def test_register_post(client):

    response = client.post(
        reverse("register"),
        {
            "username": "ali",
            "first_name": "Ali",
            "last_name": "Hassan",
            "email": "ali@test.com",
            "birth_date": "2000-01-01",
            "gender": "M",
            "phone": "0600000000",
            "password1": "StrongPassword123",
            "password2": "StrongPassword123",
        },
    )

    assert response.status_code == 302

    assert User.objects.count() == 1
    assert Patient.objects.count() == 1