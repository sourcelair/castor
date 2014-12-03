"""
This module defines the Castor server, that consumes the Docker events from
a given host.
"""

from datetime import datetime
from settings import SETTINGS
import docker
import json
import tasks


DOCKER_SETTINGS = SETTINGS.get('docker', {})
DOCKER_CLIENT_KWARGS = {}

for setting in DOCKER_SETTINGS:
    DOCKER_CLIENT_KWARGS[setting] = DOCKER_SETTINGS[setting]

# Customize the Docker client according to settings in `settings.json`
DOCKER_CLIENT = docker.Client(**DOCKER_CLIENT_KWARGS)

# Define the events endpoint according to the last dispatched event (if any)
EVENTS_ENDPOINT = '/events'
LAST_EVENT = tasks.get_last_event()

if LAST_EVENT and LAST_EVENT.get('time'):
    EVENTS_ENDPOINT += '?since=%s' % (LAST_EVENT['time'] + 1)

EVENTS_URL = DOCKER_CLIENT._url(EVENTS_ENDPOINT)
EVENTS_REQUEST = DOCKER_CLIENT.get(EVENTS_URL, stream=True)
EVENTS_STREAM = DOCKER_CLIENT._stream_helper(EVENTS_REQUEST)

print 'Start consuming events from %s' % EVENTS_URL

try:
    for event in EVENTS_STREAM:
        event = json.loads(event)
        time = datetime.now()  # Time of event receipt
        status = event['status']  # Event status
        container = event['id'][:10]  # Container that emitted the event
        print '[%s] Received event (%s - %s)' % (time, status, container)
        tasks.dispatch_event.delay(event)
except KeyboardInterrupt:
    # Do not display ugly exception if stopped with Ctrl + C
    print '\rBye.'

