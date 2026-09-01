from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from appointments.models import Appointment

try:
    from no_show_ML.predict import predict_appointment_no_show
except Exception:
    predict_appointment_no_show = None


@receiver(post_save, sender=Appointment)
def appointment_post_save(sender, instance, created, **kwargs):
    """When an appointment is created or updated ensure we have a predicted_no_show value."""
    if predict_appointment_no_show is None:
        return

    # If newly created or no prediction yet, compute prediction
    if created or instance.predicted_no_show in (None, ''):
        try:
            prob = predict_appointment_no_show(instance)
            if prob is not None:
                instance.predicted_no_show = prob
                instance.save(update_fields=['predicted_no_show'])
        except Exception:
            # be safe: don't crash on prediction errors
            pass
