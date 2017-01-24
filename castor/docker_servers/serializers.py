from rest_framework import serializers

from docker_servers.models import DockerServer


class DockerServerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DockerServer
        fields = (
            'id', 'url', 'name', 'version', 'docker_host', 'docker_tls_verify',
            'docker_cert_path'
        )
