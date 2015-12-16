"""
This module defines the Castor server, that consumes the Docker events from
a given host. This module can be run as a command line script or get imported
by another Python script.
"""
import docker
import tasks
import settings


DOCKER_SETTINGS = settings.SETTINGS.get('docker', {})
# Customize the Docker client according to settings in `settings.json`
DOCKER_CLIENT = docker.Client(**DOCKER_SETTINGS)


def consume():
    """
    Starts consuming Docker events accoding to the already defined settings.
    """
    print 'Start consuming events from %s' % DOCKER_SETTINGS['base_url']
    for event in DOCKER_CLIENT.events(decode=True):
        for hook in settings.HOOKS:
            tasks.dispatch_event.delay(event, hook)


if __name__ == '__main__':
    try:
        consume()
    except KeyboardInterrupt:
        # Do not display ugly exception if stopped with Ctrl + C
        print '\rBye.'
