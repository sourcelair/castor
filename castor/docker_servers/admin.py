from django.contrib import admin

from docker_servers.models import DockerServer


@admin.register(DockerServer)
class DockerServerAdmin(admin.ModelAdmin):
    pass
