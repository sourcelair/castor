from django.db import models

from docker_servers.models import DockerServer
from docker_events.models import DockerEvent


class WebHook(models.Model):
    docker_server = models.ForeignKey(DockerServer)
    payload_url = models.CharField(max_length=255)


class Notification(models.Model):
    webhook = models.ForeignKey(WebHook)
    docker_event = models.ForeignKey(DockerEvent)
    dispatched_at = models.DateTimeField(auto_now=True)
    delivery_duration = models.IntegerField()
    request_headers = models.CharField(max_length=65535)
    request_body = models.CharField(max_length=65535)
    response_headers = models.CharField(max_length=65535)
    response_body = models.CharField(max_length=65535)
