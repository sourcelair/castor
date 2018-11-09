from rest_framework import viewsets
from rest_framework import renderers

from webhooks.models import WebHook
from webhooks.serializers import WebHookSerializer


class WebHookViewSet(viewsets.ModelViewSet):
    queryset = WebHook.objects.all()
    serializer_class = WebHookSerializer
