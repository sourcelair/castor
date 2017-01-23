import json

from django.core.management.base import BaseCommand, CommandError

from docker_events.models import DockerEvent
from docker_events.tasks import dispatch_docker_event
from docker_servers.models import DockerServer


class Command(BaseCommand):
    help = 'Watch for Docker events in the available servers'

    def handle(self, *args, **options):
        # Right now this works just for the first servers, since we are mainly
        # in prototyping stage.
        # TODO: Make this work for all servers
        server = DockerServer.objects.first()
        docker_client = server.get_client()

        for event in docker_client.events():
            json_event = json.loads(event)
            docker_event = DockerEvent.objects.create(
                docker_server=server,
                data=json_event
            )
            dispatch_docker_event.delay(docker_event.id)
            self.stdout.write(str(json_event))
