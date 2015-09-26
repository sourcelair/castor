from redis import Redis
from rq.decorators import job
import requests
import settings


redis_conn = Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


@job('castor', connection=redis_conn)
def dispatch_event(event):
    event_tuple = (event['status'], event['id'][:10])
    print 'Dispatching "%s" event for container "%s"' % event_tuple

    for hook in settings.HOOKS:
        requests.post(hook, data=event)

    result = 'Dispatched %s:%s at %s destinations' % (
        event_tuple[0], event_tuple[1], len(settings.HOOKS)
    )
    return result
