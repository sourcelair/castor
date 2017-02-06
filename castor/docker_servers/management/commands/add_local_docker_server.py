from django.core.management.base import BaseCommand, CommandError

from docker_servers.models import DockerServer


class Command(BaseCommand):
    help = 'Add a Docker Server for the local Docker socket'

    def handle(self, *args, **options):
        server = DockerServer.objects.create(
            name='localhost',
            docker_host='unix://var/run/docker.sock',
            docker_tls_verify=False
        )
