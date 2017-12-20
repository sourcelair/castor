from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from docker_servers.models import DockerServer

from webhooks.tasks import dispatch_docker_event


class Command(BaseCommand):
    help = 'Capture Docker events in the available servers'

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

        events_kwargs = {
            'decode': True
        }

        docker_client = server.get_client()

        for docker_event in docker_client.events(**events_kwargs):
            try:
                dispatch_docker_event.delay(docker_event, server)
                self.stdout.write(str(docker_event))
            except IntegrityError as e:
                # This means that the event has been already captured and saved
                # into the database, so we just omit this message.
                # This is caused when using the --resume argument.
                if 'duplicate key value' in str(e):
                    pass
