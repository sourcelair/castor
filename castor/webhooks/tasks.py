from datetime import datetime

import requests
from celery import shared_task

from webhooks.models import Delivery
from webhooks.models import WebHook


@shared_task
def dispatch_docker_event_to_webhook(docker_event, webhook_id):
    """
    Dispatch the Docker event to the WebHook identified by the given id.
    """
    webhook = WebHook.objects.get(id=webhook_id)

    data = {
        'event': docker_event,
        'docker_server': webhook.docker_server.name
    }
    dispatched_at = datetime.now()

    try:
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
        delivery = Delivery.objects.create(
            webhook=webhook,
            dispatched_at=dispatched_at,
            delivered=True,
            delivery_duration=duration_in_ms,
            status_code=response.status_code,
            request_headers=dict(response.request.headers),
            request_body=response.request.body,
            response_headers=dict(response.headers),
            response_body=response.text
        )
    except Exception as e:
        delivery = Delivery.objects.create(
            webhook=webhook,
            dispatched_at=dispatched_at,
            delivered=False,
            failure_reason=str(e),
            delivery_duration=0,
            request_headers=None,
            request_body=None,
            response_headers=None,
            response_body=None
        )

    return delivery.id


@shared_task
def dispatch_docker_event(docker_event, docker_server):
    """
    Dispatch the Docker event to all WebHooks subscribed to the Docker
    server's events.
    """
    webhooks = WebHook.objects.filter(docker_server=docker_server)

    for webhook in webhooks:
        dispatch_docker_event_to_webhook.delay(docker_event, webhook.id)
