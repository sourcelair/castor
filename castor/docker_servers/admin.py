from django.contrib import admin

from docker_servers.models import DockerServer

class DockerServerAdmin(admin.ModelAdmin):
    pass
admin.site.register(DockerServer, DockerServerAdmin)
