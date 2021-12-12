from django.apps import AppConfig


class OauthConfig(AppConfig):
    name = "oauth"

    def register_signals(self):
        from . import signals

    def ready(self):
        self.register_signals()
