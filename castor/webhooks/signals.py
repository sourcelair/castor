from django.db.models.signals import post_save
from django.dispatch import receiver

from docker_events.models import DockerEvent
from webhooks.tasks import dispatch_docker_event


@receiver(post_save, sender=DockerEvent)
def dispatch_new_docker_events(sender, **kwargs):
    """
    Every time a new Docker event is being saved in the database, dispatch it.
    """
    if kwargs['created']:
        dispatch_docker_event.delay(kwargs['instance'].id)
