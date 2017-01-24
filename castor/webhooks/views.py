from rest_framework import viewsets
from rest_framework import renderers

from webhooks.models import Delivery
from webhooks.models import WebHook
from webhooks.serializers import DeliverySerializer
from webhooks.serializers import WebHookSerializer


class WebHookViewSet(viewsets.ModelViewSet):
    queryset = WebHook.objects.all()
    serializer_class = WebHookSerializer


class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer


class WebHookDeliveryViewSet(viewsets.ModelViewSet):
    renderer_classes = (
        renderers.JSONRenderer,
        renderers.BrowsableAPIRenderer,
        renderers.TemplateHTMLRenderer
    )
    serializer_class = DeliverySerializer
    template_name = 'webhooks/components/delivery.html'

    def get_queryset(self):
        webhook = WebHook.objects.get(id=self.kwargs['webhook_id'])
        return Delivery.objects.filter(webhook=webhook)
