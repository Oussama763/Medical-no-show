# Medical No-Show

Medical No-Show is an appointment management system with a built-in machine
learning pipeline to predict patient no-shows. The project stores bookings,
tracks attendance, and collects clinical and location flags for future model
features.

Features
--------
- Patient and doctor accounts with email verification
- Booking calendar and time slot management
- Attendance recording (doctor/admin enforced)
- Clinical flags (diabetes, hypertension, handicapped) and location capture
- ML pipeline: train/predict models for no-show risk and record model history

Tech stack
----------
- Django (web framework)
- SQLite / PostgreSQL (database)
- scikit-learn, pandas, joblib (ML training and persistence)
- Bootstrap + Chart.js (UI and analytics)

Installation
------------
1. Create and activate a Python virtual environment (recommended).

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run migrations and create a superuser:

```bash
PYTHONPATH=src python3 src/manage.py migrate
PYTHONPATH=src python3 src/manage.py createsuperuser
```

4. (Optional) Train ML models:

```bash
PYTHONPATH=src python3 -m no_show_ML.train
```

5. Run the development server:

```bash
PYTHONPATH=src python3 src/manage.py runserver
```

For production, configure a proper database, secret key, and static file hosting.


