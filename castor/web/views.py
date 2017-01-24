from django.shortcuts import render

from webhooks.models import Delivery
from webhooks.models import WebHook


def home(request):
    deliveries = Delivery.objects.all().order_by('-id')[:25]
    context = {
        'deliveries': deliveries
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
        'deliveries': Delivery.objects.order_by('-id')[:100]
    }
    return render(request, 'web/webhook.html', context=context)
