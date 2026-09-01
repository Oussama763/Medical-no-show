from django.apps import AppConfig
import threading
import time
from django.conf import settings
from django.core.management import call_command


class AppointmentsConfig(AppConfig):
    name = 'appointments'
    def ready(self):
        # import signals so they are registered
        try:
            from . import signals  # noqa: F401
        except Exception:
            pass

        # Optional: start a lightweight background retrain scheduler if enabled
        try:
            if getattr(settings, 'AUTO_RETRAIN', False):
                interval = int(getattr(settings, 'AUTO_RETRAIN_INTERVAL_SECONDS', 24 * 3600))

                def _runner():
                    while True:
                        try:
                            call_command('retrain_models')
                        except Exception:
                            pass
                        time.sleep(interval)

                t = threading.Thread(target=_runner, daemon=True)
                t.start()
        except Exception:
            pass
