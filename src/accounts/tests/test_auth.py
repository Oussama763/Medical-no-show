import pytest
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from appointments.models import Patient


@pytest.mark.django_db
def test_dashboard_requires_login(client):

    response = client.get(reverse("dashboard"))

    assert response.status_code == 302



@pytest.mark.django_db
def test_dashboard_authenticated(client):

    user = User.objects.create_user(
        username="patient",
        password="StrongPassword123",
    )

    Patient.objects.create(
        user=user,
        birth_date=date(2000, 1, 1),
        gender="M",
        phone="0611111111",
    )

    client.login(
        username="patient",
        password="StrongPassword123",
    )

    response = client.get(reverse("dashboard"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_logout_redirects_to_login(client):
    user = User.objects.create_user(
        username="patient",
        password="StrongPassword123",
    )

    Patient.objects.create(
        user=user,
        birth_date=date(2000, 1, 1),
        gender="M",
        phone="0611111111",
    )

    client.login(username="patient", password="StrongPassword123")

    response = client.post(reverse("logout"))

    assert response.status_code == 302
    assert response.url == "/accounts/login/"