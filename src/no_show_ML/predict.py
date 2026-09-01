import os
import joblib
import numpy as np
from datetime import date

from .preprocessing import load_and_preprocess


MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
BEST_MODEL_PATH = os.path.join(MODEL_DIR, 'best_model.pkl')


def load_best_model():
    if os.path.exists(BEST_MODEL_PATH):
        return joblib.load(BEST_MODEL_PATH)
    # fallback: try to load random_forest
    fallback = os.path.join(MODEL_DIR, 'random_forest.pkl')
    if os.path.exists(fallback):
        return joblib.load(fallback)
    return None


def build_feature_vector(appointment):
    """
    appointment: Appointment model instance
    Returns feature vector matching training features ordering.
    """
    patient = appointment.patient
    slot = appointment.slot

    # Age at appointment day
    birth = getattr(patient, 'birth_date', None)
    if birth is not None and hasattr(birth, 'year'):
        born = birth
        appt_date = slot.date
        age_years = appt_date.year - born.year - ((appt_date.month, appt_date.day) < (born.month, born.day))
    else:
        age_years = getattr(patient, 'age', 30)

    # Gender stored on Patient as single-char code
    gender_F = 1 if getattr(patient, 'gender', None) == 'F' else 0
    # our Patient model stores flags directly
    hypertension = 1 if getattr(patient, 'hypertension', False) else 0
    diabetes = 1 if getattr(patient, 'diabetes', False) else 0
    alcoholism = 0
    handicap = 1 if getattr(patient, 'handicapped', False) else 0
    sms_received = 0

    # wait_days: scheduling -> appointment. Use booking_date stored in appointment.booking_date
    try:
        wait_days = (slot.date - appointment.booking_date.date()).days
    except Exception:
        wait_days = 0

    # Order: Age, Hypertension, Diabetes, Alcoholism, Handicap, SMS_received, wait_days, gender_F
    features = [age_years, hypertension, diabetes, alcoholism, handicap, sms_received, wait_days, gender_F]
    return np.array(features).reshape(1, -1)


def predict_appointment_no_show(appointment):
    model = load_best_model()
    if model is None:
        return None
    x = build_feature_vector(appointment)
    try:
        prob = model.predict_proba(x)[0][1]
    except Exception:
        # model may not support predict_proba
        pred = model.predict(x)[0]
        prob = float(pred)
    return float(prob)


if __name__ == '__main__':
    print('No-show prediction helper')
