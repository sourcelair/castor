from __future__ import unicode_literals
import json

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from docker_servers.models import DockerServer


@python_2_unicode_compatible
class DockerEvent(models.Model):
    docker_server = models.ForeignKey(to=DockerServer)
    capture_time = models.DateTimeField(auto_now=True)
    data = JSONField(default={}, unique=True)

    def __str__(self):
        return 'Docker event on %s at %s' % (
            self.docker_server.name, self.capture_time
        )
