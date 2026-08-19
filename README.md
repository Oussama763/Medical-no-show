# This is a project for managing appointments

Project Structure:
```
.
├── interface
│   ├── accounts
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── templates
│   │   │   ├── dashboard.html
│   │   │   └── registration
│   │   │       ├── login.html
│   │   │       └── register.html
│   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── test_auth.py
│   │   │   ├── test_forms.py
│   │   │   └── test_views.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── appointments
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   ├── 0001_initial.py
│   │   │   ├── 0002_patient_timeslot_appointment.py
│   │   │   ├── 0003_remove_doctor_email_remove_doctor_first_name_and_more.py
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── test_appointments.py
│   │   │   ├── test_models.py
│   │   │   └── test_relationships.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── dashboard
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── templates
│   │   │   └── dashboard
│   │   │       ├── admin
│   │   │       │   └── dashboard.html
│   │   │       ├── doctor
│   │   │       │   └── dashboard.html
│   │   │       └── patient
│   │   │           └── dashboard.html
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── interface
│   │   ├── asgi.py
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── manage.py
├── README.md
└── requirements.txt

```
