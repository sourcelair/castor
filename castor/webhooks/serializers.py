from rest_framework import serializers

from docker_servers.serializers import DockerServerSerializer
from webhooks.models import WebHook


class WebHookSerializer(serializers.HyperlinkedModelSerializer):
    docker_server = DockerServerSerializer(read_only=True)

    class Meta:
        model = WebHook
        fields = (
            'id', 'url', 'docker_server', 'payload_url',
        )
