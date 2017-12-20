from rest_framework import serializers

from docker_servers.serializers import DockerServerSerializer
from webhooks.models import Delivery
from webhooks.models import WebHook


class WebHookSerializer(serializers.HyperlinkedModelSerializer):
    docker_server = DockerServerSerializer(read_only=True)
    deliveries_url = serializers.HyperlinkedIdentityField(
        read_only=True,
        view_name='webhook-delivery-list',
        lookup_field='id',
        lookup_url_kwarg='webhook_id'
    )

    class Meta:
        model = WebHook
        fields = (
            'id', 'url', 'docker_server', 'payload_url', 'deliveries_url'
        )


class DeliverySerializer(serializers.HyperlinkedModelSerializer):
    webhook = WebHookSerializer(read_only=True)

    class Meta:
        model = Delivery
        fields = (
            'id', 'url', 'webhook', 'dispatched_at', 'delivered',
            'failure_reason', 'delivery_duration', 'request_headers',
            'request_body', 'status_code', 'response_headers',
            'response_body',
        )
