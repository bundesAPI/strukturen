from django.apps import AppConfig


class OrgchartsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "orgcharts"

    def ready(self):
        from . import signals
