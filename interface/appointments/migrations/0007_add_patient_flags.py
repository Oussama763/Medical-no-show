"""Add clinical flags and email verification fields to Patient model."""
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0006_appointment_appointment_patient_44acdc_idx_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='diabetes',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='patient',
            name='hypertension',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='patient',
            name='handicapped',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='patient',
            name='email_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='patient',
            name='email_verification_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
