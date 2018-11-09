from django.contrib.postgres.fields import JSONField
from django.db import models


from docker_servers.models import DockerServer


class WebHook(models.Model):
    docker_server = models.ForeignKey(DockerServer)
    payload_url = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
