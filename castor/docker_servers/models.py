from django.db import models
import docker


class DockerServer(models.Model):
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=255, default='auto')
    docker_host = models.CharField(max_length=255)
    docker_tls_verify = models.BooleanField(default=True)
    docker_cert_path = models.CharField(max_length=255, null=True, blank=True)

    def get_env(self):
        env = {
            'DOCKER_HOST': self.docker_host
        }

        if self.docker_tls_verify:
            env['DOCKER_TLS_VERIFY'] = self.docker_tls_verify

        if self.docker_cert_path:
            env['DOCKER_CERT_PATH'] = self.docker_cert_path

        return env

    def get_client(self):
        client = docker.from_env(
            version=self.version,
            environment=self.get_env()
        )
        return client
