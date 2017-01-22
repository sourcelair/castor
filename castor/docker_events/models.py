from __future__ import unicode_literals
import json

from django.db import models

from docker_servers.models import DockerServer


class DockerEvent(models.Model):
    docker_server = models.ForeignKey(to=DockerServer)
    capture_time = models.DateTimeField(auto_now=True)
    data = models.CharField(max_length=65535)

    def get_json_data(self):
        return json.dumps(self.data)

    def __unicode__(self):
        return 'Docker event on %s at %s' % (
            self.docker_server.name, self.capture_time
        )

    def __str__(self):
        return self.__unicode__()
