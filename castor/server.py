from datetime import datetime
import docker
import json
import tasks


SETTINGS_FILE = open('settings.json')
SETTINGS = json.loads(SETTINGS_FILE.read())
SETTINGS_FILE.close()  # We don't have to keep the file open anymore

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
    # TODO: Fire dispatcing task
