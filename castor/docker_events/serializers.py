from rest_framework import serializers

from docker_events.models import DockerEvent
from docker_servers.serializers import DockerServerSerializer


class DockerEventSerializer(serializers.HyperlinkedModelSerializer):
    docker_server = DockerServerSerializer(read_only=True)

    class Meta:
        model = DockerEvent
        fields = ('id', 'url', 'docker_server', 'capture_time', 'data')
