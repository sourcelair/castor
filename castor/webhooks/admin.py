from django.contrib import admin

from webhooks.models import Delivery
from webhooks.models import WebHook


class WebhookAdmin(admin.ModelAdmin):
    pass
admin.site.register(WebHook, WebhookAdmin)


class DeliveryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Delivery, DeliveryAdmin)
