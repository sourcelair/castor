"""
This module defines the Castor server, that consumes the Docker events from
a given host. This module can be run as a command line script or get imported
by another Python script.
"""
import docker
import redis
import settings
import tasks


def consume(docker_client, redis_client):
    """
    Starts consuming Docker events accoding to the already defined settings.
    """
    print 'Start consuming events from %s' % docker_client.base_url
    since = redis_client.get('castor:last_event')
    for event in docker_client.events(decode=True, since=since):
        for hook in settings.HOOKS:
            tasks.dispatch_event.delay(event, hook)
        redis_client.set('castor:last_event', event['time'])


if __name__ == '__main__':
    try:
        docker_client = docker.Client(**settings.SETTINGS.get('docker', {}))
        redis_client = redis.StrictRedis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
        )
        consume(docker_client, redis_client)
    except KeyboardInterrupt:
        # Do not display ugly exception if stopped with Ctrl + C
        print '\rBye.'
