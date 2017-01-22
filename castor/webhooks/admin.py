from django.contrib import admin

from webhooks.models import Notification
from webhooks.models import WebHook


class WebhookAdmin(admin.ModelAdmin):
    pass
admin.site.register(WebHook, WebhookAdmin)


class NotificationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Notification, NotificationAdmin)
