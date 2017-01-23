from datetime import datetime

import requests
from celery import shared_task

from docker_events.models import DockerEvent
from webhooks.models import Notification
from webhooks.models import WebHook

@shared_task
def dispatch_docker_event(docker_event_id):
    docker_event = DockerEvent.objects.get(id=docker_event_id)
    webhooks = WebHook.objects.all()
    for webhook in webhooks:
        data = {
            'event': docker_event.data,
            'capture_time': int(docker_event.capture_time.timestamp())
        }
        dispatched_at = datetime.now()
        try:
            response = requests.post(
                url=webhook.payload_url,
                json=data
            )
            end = datetime.now()
            duration_timedelta = end - dispatched_at
            duration_in_ms = int(duration_timedelta.total_seconds() * 1000)
            Notification.objects.create(
                webhook=webhook,
                docker_event=docker_event,
                dispatched_at=dispatched_at,
                delivered=True,
                delivery_duration=duration_in_ms,
                request_headers=dict(response.request.headers),
                request_body=response.request.body,
                response_headers=dict(response.headers),
                response_body=response.text
            )
        except Exception as e:
            Notification.objects.create(
                webhook=webhook,
                docker_event=docker_event,
                dispatched_at=dispatched_at,
                delivered=False,
                failure_reason=str(e),
                delivery_duration=0,
                request_headers=None,
                request_body=None,
                response_headers=None,
                response_body=None
            )
