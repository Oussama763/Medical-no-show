import os
import sys
import json
from datetime import datetime

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Append new appointment data to the training CSV and retrain ML models.'

    def handle(self, *args, **options):
        # Ensure project src path is on sys.path so we can import no_show_ML
        src_path = str(settings.BASE_DIR)
        if src_path not in sys.path:
            sys.path.insert(0, src_path)

        # Locate CSV under the src package
        csv_path = os.path.join(src_path, 'no_show_ML', 'data', 'noshowappointments.csv')

        # Import local Django models lazily to avoid circular imports
        from appointments.models import Appointment, ModelTrainingHistory
        import pandas as pd

        # Determine last ScheduledDay in CSV to avoid duplicates
        if os.path.exists(csv_path):
            try:
                df = pd.read_csv(csv_path, parse_dates=['ScheduledDay'], low_memory=False)
                if 'ScheduledDay' in df.columns and not df['ScheduledDay'].isna().all():
                    max_scheduled = df['ScheduledDay'].max()
                else:
                    max_scheduled = None
            except Exception:
                max_scheduled = None
        else:
            self.stdout.write(self.style.WARNING(f'CSV not found at {csv_path}, aborting.'))
            return

        # Collect new appointments after max_scheduled (or all if unknown)
        if max_scheduled is not None:
            new_appts = Appointment.objects.filter(booking_date__gt=max_scheduled)
        else:
            new_appts = Appointment.objects.all()

        if not new_appts.exists():
            self.stdout.write('No new appointments to append to dataset.')
        else:
            rows = []
            # Read CSV columns so appended rows match original dataset structure
            existing_cols = pd.read_csv(csv_path, nrows=0).columns.tolist()

            for a in new_appts.select_related('patient'):
                p = a.patient
                appt_day = a.slot.date
                scheduled = a.booking_date
                # compute age at appointment
                age = 30
                try:
                    born = p.birth_date
                    age = appt_day.year - born.year - ((appt_day.month, appt_day.day) < (born.month, born.day))
                except Exception:
                    pass

                # Construct a full-row dict matching existing_cols
                row = {c: '' for c in existing_cols}

                # Map known fields
                if 'PatientId' in row:
                    row['PatientId'] = p.pk
                if 'AppointmentID' in row:
                    row['AppointmentID'] = a.pk
                if 'Gender' in row:
                    row['Gender'] = p.gender
                if 'ScheduledDay' in row:
                    row['ScheduledDay'] = scheduled.isoformat()
                if 'AppointmentDay' in row:
                    row['AppointmentDay'] = datetime.combine(appt_day, datetime.min.time()).isoformat()
                if 'Age' in row:
                    row['Age'] = age
                if 'Hipertension' in row:
                    row['Hipertension'] = 1 if p.hypertension else 0
                if 'Diabetes' in row:
                    row['Diabetes'] = 1 if p.diabetes else 0
                if 'Alcoholism' in row:
                    row['Alcoholism'] = 0
                if 'Handcap' in row:
                    row['Handcap'] = 1 if p.handicapped else 0
                if 'SMS_received' in row:
                    row['SMS_received'] = 0
                if 'No-show' in row:
                    row['No-show'] = 'Yes' if a.status == a.NO_SHOW else 'No'
                rows.append(row)

            if rows:
                append_df = pd.DataFrame(rows)
                append_df.to_csv(csv_path, mode='a', header=False, index=False)
                self.stdout.write(self.style.SUCCESS(f'Appended {len(rows)} rows to {csv_path}'))

        # Now run training by importing the training module
        try:
            from no_show_ML.train import train_all

            results, best = train_all(csv_path)

            # Save a training history record
            acc = results.get(best)
            m = ModelTrainingHistory.objects.create(model_name=best, accuracy=acc, details=results, data_until=datetime.utcnow())
            self.stdout.write(self.style.SUCCESS(f'Retrained models. Best: {best} acc={acc}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Training failed: {e}'))