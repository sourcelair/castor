from rest_framework import viewsets

from docker_events.models import DockerEvent
from docker_events.serializers import DockerEventSerializer


class DockerEventViewSet(viewsets.ModelViewSet):
    queryset = DockerEvent.objects.all()
    serializer_class = DockerEventSerializer
