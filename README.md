# This is a project for managing appointments

Project Structure:
```
Medical-no-show/
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
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── test_appointments.py
│   │   │   ├── test_models.py
│   │   │   └── test_relationships.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── db.sqlite3
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
