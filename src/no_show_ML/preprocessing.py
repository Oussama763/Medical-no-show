import pandas as pd

def load_and_preprocess(csv_path):
    df = pd.read_csv(csv_path)

    # Keep only columns that reflect patient-provided or booking-provided info
    # Columns in dataset: Gender, ScheduledDay, AppointmentDay, Age, Hipertension,
    # Diabetes, Alcoholism, Handcap, SMS_received, No-show
    df = df.copy()

    # Parse datetimes
    df['ScheduledDay'] = pd.to_datetime(df['ScheduledDay'])
    df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay'])

    # Compute wait days between scheduling and appointment
    df['wait_days'] = (df['AppointmentDay'] - df['ScheduledDay']).dt.days

    # Normalize column names (typos)
    if 'Hipertension' in df.columns:
        df['Hypertension'] = df['Hipertension']
    elif 'Hypertension' in df.columns:
        df['Hypertension'] = df['Hypertension']

    # Handcap -> Handicap
    if 'Handcap' in df.columns:
        df['Handicap'] = df['Handcap']

    # Target: No-show -> 1 if 'Yes' else 0
    df['no_show_target'] = df['No-show'].map(lambda x: 1 if str(x).strip().lower() in {'yes','y','1','true'} else 0)

    # Select features
    features = ['Age', 'Gender', 'Hypertension', 'Diabetes', 'Alcoholism', 'Handicap', 'SMS_received', 'wait_days']
    df = df[features + ['no_show_target']].copy()

    # Gender -> binary: F=1, M=0
    df['gender_F'] = df['Gender'].map(lambda x: 1 if str(x).strip().upper() == 'F' else 0)
    df = df.drop(columns=['Gender'])

    # Fill missing
    df = df.fillna(0)

    X = df.drop(columns=['no_show_target'])
    y = df['no_show_target']

    return X, y
