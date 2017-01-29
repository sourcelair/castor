import json

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from docker_events.models import DockerEvent
from docker_events.tasks import dispatch_docker_event
from docker_servers.models import DockerServer


class Command(BaseCommand):
    help = 'Watch for Docker events in the available servers'

    def add_arguments(self, parser):
        parser.add_argument(
            'docker_server', nargs='?', type=str, default='localhost'
            )
        parser.add_argument(
            '--resume',
            action='store_true',
            dest='resume',
            default=False,
            help='Resume from the last event captured on this Docker server',
        )

    def handle(self, *args, **options):
        server = DockerServer.objects.get(
            name=options['docker_server']
        )

        if options.get('resume'):
            last_event = DockerEvent.objects.filter(
                docker_server=server
            ).order_by('-capture_time').first()

            events_kwargs = {
                'since': last_event.data['time']
            }
        else:
            events_kwargs = {}
        docker_client = server.get_client()

        for event in docker_client.events(**events_kwargs):
            json_event = json.loads(event.decode('utf-8'))
            try:
                docker_event = DockerEvent.objects.create(
                    docker_server=server,
                    data=json_event
                )
            except IntegrityError as e:
                if 'duplicate key value' in str(e):
                    pass
            else:
                dispatch_docker_event.delay(docker_event.id)
                self.stdout.write(str(json_event))
