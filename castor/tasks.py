from celery import Celery
import requests
import settings

BROKER_URL = 'redis://%s:%s/%s' % (
    settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_DB
)

app = Celery('castor', broker=BROKER_URL)

@app.task
def dispatch_event(event):
    event_tuple = (event['status'], event['id'][:10])
    print 'Dispatching "%s" event for container "%s"' % event_tuple

    for hook in settings.HOOKS:
        requests.post(hook, data=event)

    result = 'Dispatched %s:%s at %s destinations' % (
        event_tuple[0], event_tuple[1], len(settings.HOOKS)
    )
    return result
