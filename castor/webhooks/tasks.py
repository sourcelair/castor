from datetime import datetime
import logging

from celery import shared_task
import requests

from docker_servers.models import DockerServer
from webhooks.models import WebHook


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

@shared_task
def dispatch_docker_event_to_webhook(docker_event, webhook_id):
    """
    Dispatch the Docker event to the WebHook identified by the given id.
    """
    LOGGER.debug(f'Dispatching Docker Event {docker_event} to WebHook #{webhook_id}.')
    webhook = WebHook.objects.get(id=webhook_id)

    data = {
        'event': docker_event,
        'docker_server': webhook.docker_server.name
    }
    dispatched_at = datetime.now()

    try:
        LOGGER.debug(f'Sending POST request to {webhook.payload_url} with payload {data}.')
        response = requests.post(
            url=webhook.payload_url,
            json=data,
            headers={
                'user-agent': 'Castor/0.1 via python-requests/2.12.5'
            }
        )
        end = datetime.now()
        duration_timedelta = end - dispatched_at
        duration_in_ms = int(duration_timedelta.total_seconds() * 1000)
        LOGGER.INFO(f'({response.status_code}) Successfully sent {data} to {webhook.payload_url}.')
        return {
            'webhook': webhook.pk,
            'dispatched_at': dispatched_at,
            'delivered': True,
            'delivery_duration': duration_in_ms,
            'status_code': response.status_code,
            'request_headers': dict(response.request.headers),
            'request_body': response.request.body,
            'response_headers': dict(response.headers),
            'response_body': response.text,
        }
    except Exception as e:
        LOGGER.INFO(f'Could not send {data} to {webhook.payload_url}: {e}.')
        return {
            'webhook': webhook,
            'dispatched_at': dispatched_at,
            'delivered': False,
            'failure_reason': str(e),
            'delivery_duration': 0,
            'request_headers': None,
            'request_body': None,
            'response_headers': None,
            'response_body': None
        }


@shared_task
def dispatch_docker_event(docker_event, docker_server_pk):
    """
    Dispatch the Docker event to all WebHooks subscribed to the Docker
    server's events.
    """
    docker_server = DockerServer.objects.get(pk=docker_server_pk)
    webhooks = WebHook.objects.filter(docker_server=docker_server)

    for webhook in webhooks:
        dispatch_docker_event_to_webhook.delay(docker_event, webhook.id)
