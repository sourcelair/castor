from django.contrib import admin

from docker_events.models import DockerEvent

class DockerEventAdmin(admin.ModelAdmin):
    pass
admin.site.register(DockerEvent, DockerEventAdmin)
