from django.shortcuts import render

from webhooks.models import Notification
from webhooks.models import WebHook


def home(request):
    notifications = Notification.objects.all().order_by('-id')[:25]
    context = {
        'notifications': notifications
    }
    return render(request, 'web/index.html', context=context)


def webhooks(request):
    webhooks = WebHook.objects.all()
    context = {
        'webhooks': webhooks
    }
    return render(request, 'web/webhooks.html', context=context)

def webhook(request, webhook_id):
    webhook = WebHook.objects.get(id=webhook_id)
    context = {
        'webhook': webhook,
        'notifications': Notification.objects.order_by('-id')[:100]
    }
    return render(request, 'web/webhook.html', context=context)
