from django.shortcuts import render

from webhooks.models import Notification


def home(request):
    notifications = Notification.objects.all().order_by('-id')[:25]
    context = {
        'notifications': notifications
    }
    return render(request, 'web/index.html', context=context)
