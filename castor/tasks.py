import requests
import settings

from celery import Celery
from celery.utils.log import get_task_logger


LOGGER = get_task_logger(__name__)

app = Celery('castor', )

@app.task
def dispatch_event(event, hook):
    event_tuple = (event['status'], event['id'][:10], hook)
    LOGGER.info('Dispatching "%s" for "%s" to %s', event['status'],
                event['id'][:10], hook)
    requests.post(hook, json=event)
    result = 'Delivered "%s" for "%s" to %s' % event_tuple
    LOGGER.info(result)
    return {'result': result}
