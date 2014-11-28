from datetime import datetime
from settings import SETTINGS
import docker
import json
import tasks


DOCKER_SETTINGS = SETTINGS.get('docker', {})
DOCKER_CLIENT_KWARGS = {}

for setting in DOCKER_SETTINGS:
    DOCKER_CLIENT_KWARGS[settings] = DOCKER_SETTINGS[setting]

DOCKER_CLIENT = docker.Client(**DOCKER_CLIENT_KWARGS)

for event in DOCKER_CLIENT.events():
    event = json.loads(event)
    time = datetime.now()  # Time of event receipt
    status = event['status']  # Event status
    container = event['id'][:10]  # Container that emitted the event
    print '[%s] Received event (%s - %s)' % (time, status, container)
    tasks.dispatch_event(event)
