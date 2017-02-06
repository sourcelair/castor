from django.apps import AppConfig

class WebhooksConfig(AppConfig):
    name = 'webhooks'

    def ready(self):
        from webhooks import signals
