from django.shortcuts import render
from rest_framework import viewsets

from docker_servers.models import DockerServer
from docker_servers.serializers import DockerServerSerializer


class DockerServerViewSet(viewsets.ModelViewSet):
    queryset = DockerServer.objects.all()
    serializer_class = DockerServerSerializer
