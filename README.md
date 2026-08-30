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
│   │   │   ├── 0003_remove_doctor_email_remove_doctor_first_name_and_more.py
│   │   │   ├── 0004_timeslot_is_available.py
│   │   │   ├── 0005_doctor_appointment_duration_alter_doctor_user.py
│   │   │   ├── 0006_appointment_appointment_patient_44acdc_idx_and_more.py
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── test_appointments.py
│   │   │   ├── test_models.py
│   │   │   ├── test_patient_booking.py
│   │   │   └── test_relationships.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── dashboard
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── decorators.py
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── static
│   │   │   └── dashboard
│   │   │       ├── css
│   │   │       │   └── style.css
│   │   │       └── js
│   │   ├── templates
│   │   │   └── dashboard
│   │   │       ├── admin
│   │   │       │   ├── dashboard.html
│   │   │       │   ├── doctor_confirm_delete.html
│   │   │       │   ├── doctor_form.html
│   │   │       │   ├── doctors.html
│   │   │       │   ├── generate_slots.html
│   │   │       │   ├── slot_confirm_delete.html
│   │   │       │   ├── slot_form.html
│   │   │       │   └── slots.html
│   │   │       ├── base.html
│   │   │       ├── doctor
│   │   │       │   └── dashboard.html
│   │   │       ├── includes
│   │   │       │   └── sidebar.html
│   │   │       └── patient
│   │   │           ├── appointments.html
│   │   │           ├── book_appointment.html
│   │   │           ├── calendar.html
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
├── pytest.ini
├── README.md
└── requirements.txt
```
