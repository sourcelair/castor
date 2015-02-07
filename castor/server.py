"""
This module defines the Castor server, that consumes the Docker events from
a given host. This module can be run as a command line script or get imported
by another Python script.
"""

from datetime import datetime
from settings import SETTINGS
import docker
import json
import os
import tasks


DOCKER_SETTINGS = SETTINGS.get('docker', {})
DOCKER_CLIENT_KWARGS = {}

for setting in DOCKER_SETTINGS:
    DOCKER_CLIENT_KWARGS[setting] = DOCKER_SETTINGS[setting]

# Customize the Docker client according to settings in `settings.json`
DOCKER_CLIENT = docker.Client(**DOCKER_CLIENT_KWARGS)

# Define the events endpoint according to the last dispatched event (if any)
last_event_file_PATH = '.data/.last-event'
EVENTS_ENDPOINT = '/events'
LAST_EVENT = None

if os.path.exists(last_event_file_PATH):
    with open(last_event_file_PATH, 'r') as last_event_file:
        try:
            LAST_EVENT = int(last_event_file.read().strip())
        except ValueError:
            pass

if LAST_EVENT:
    EVENTS_ENDPOINT += '?since=%s' % (LAST_EVENT)

EVENTS_URL = DOCKER_CLIENT._url(EVENTS_ENDPOINT)


def consume():
    """
    Starts consuming Docker events accoding to the already defined settings.
    """
    request = DOCKER_CLIENT.get(EVENTS_URL, stream=True)
    stream = DOCKER_CLIENT._stream_helper(request)

    print 'Start consuming events from %s' % EVENTS_URL

    for event in stream:
        event = json.loads(event)

        with open(last_event_file_PATH, 'w+') as last_event_file:
            last_event_file.write(str(event['time']))

        time = datetime.now()  # Time of event receipt
        status = event['status']  # Event status
        container = event['id'][:10]  # Container that emitted the event
        print '[%s] Received event (%s - %s)' % (time, status, container)
        tasks.dispatch_event.delay(event)


if __name__ == '__main__':
    try:
        consume()
    except KeyboardInterrupt:
        # Do not display ugly exception if stopped with Ctrl + C
        print '\rBye.'
