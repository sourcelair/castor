from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from webhooks.models import WebHook


@login_required
def home(request):
    return render(request, 'web/index.html')


def signin(request):
    return render(request, 'web/signin.html')


@login_required
def webhooks(request):
    webhooks = WebHook.objects.all()
    context = {
        'webhooks': webhooks
    }
    return render(request, 'web/webhooks.html', context=context)


@login_required
def webhook(request, webhook_id):
    webhook = WebHook.objects.get(id=webhook_id)
    context = {
        'webhook': webhook,
    }
    return render(request, 'web/webhook.html', context=context)
