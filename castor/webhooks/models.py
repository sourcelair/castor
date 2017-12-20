from django.contrib.postgres.fields import JSONField
from django.db import models


from docker_servers.models import DockerServer


class WebHook(models.Model):
    docker_server = models.ForeignKey(DockerServer)
    payload_url = models.CharField(max_length=255)
    active = models.BooleanField(default=True)


class Delivery(models.Model):
    webhook = models.ForeignKey(WebHook)
    dispatched_at = models.DateTimeField(auto_now=True)
    delivered = models.BooleanField(default=True)
    failure_reason = models.TextField(null=True, blank=True)
    delivery_duration = models.IntegerField()
    request_headers = JSONField(default={}, null=True)
    request_body = models.TextField(null=True, blank=True)
    status_code = models.IntegerField(default=None, null=True)
    response_headers = JSONField(default={}, null=True)
    response_body = models.TextField(null=True, blank=True)
