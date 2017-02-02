from django.contrib import admin

from webhooks.models import Delivery
from webhooks.models import WebHook


@admin.register(WebHook)
class WebhookAdmin(admin.ModelAdmin):
    pass


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    pass
