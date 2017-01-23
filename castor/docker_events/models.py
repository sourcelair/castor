from __future__ import unicode_literals
import json

from django.contrib.postgres.fields import JSONField
from django.db import models

from docker_servers.models import DockerServer


class DockerEvent(models.Model):
    docker_server = models.ForeignKey(to=DockerServer)
    capture_time = models.DateTimeField(auto_now=True)
    data = JSONField(default={})

    def __unicode__(self):
        return 'Docker event on %s at %s' % (
            self.docker_server.name, self.capture_time
        )

    def __str__(self):
        return self.__unicode__()
