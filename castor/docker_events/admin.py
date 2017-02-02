from django.contrib import admin

from docker_events.models import DockerEvent


@admin.register(DockerEvent)
class DockerEventAdmin(admin.ModelAdmin):
    pass
