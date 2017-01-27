import json

from django.core.management.base import BaseCommand, CommandError

from docker_events.models import DockerEvent
from docker_events.tasks import dispatch_docker_event
from docker_servers.models import DockerServer


class Command(BaseCommand):
    help = 'Watch for Docker events in the available servers'

    def add_arguments(self, parser):
        parser.add_argument(
            'docker_server', nargs='?', type=str, default='localhost'
            )

    def handle(self, *args, **options):
        server = DockerServer.objects.get(
            name=options['docker_server']
        )
        docker_client = server.get_client()

        for event in docker_client.events():
            json_event = json.loads(event)
            docker_event = DockerEvent.objects.create(
                docker_server=server,
                data=json_event
            )
            dispatch_docker_event.delay(docker_event.id)
            self.stdout.write(str(json_event))
