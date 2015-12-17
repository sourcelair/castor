import requests
import settings

from celery import Celery
from celery.utils.log import get_task_logger


LOGGER = get_task_logger(__name__)

app = Celery('castor', broker=settings.REDIS_URL)

@app.task(bind=True, max_retries=len(settings.RETRY_POLICY))
def dispatch_event(self, event, hook):
    success = True
    countdown = 0
    # Do this, otherwise this will crash in the last retry with index out of
    # bounds.
    if self.request.retries < len(settings.RETRY_POLICY):
        countdown = settings.RETRY_POLICY[self.request.retries]

    LOGGER.info('Dispatching "%s" for "%s" to %s', event['status'],
                event['id'][:10], hook)
    try:
        response = requests.post(hook, data=event)
        response.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        # If server error occured, log and retry
        if response.status_code >= 500:
            LOGGER.exception(
                'Delivery failed with status "%s" %s" for "%s" to %s',
                response.status_code, event['status'], event['id'][:10], hook,
            )
            raise self.retry(exc=exc, countdown=countdown)

        # If server did not accept the response, log, mark as failure and
        # don't retry
        LOGGER.error(
            'Delivery not accepted "%s" for "%s" to %s, status: %s',
            event['status'], event['id'][:10], hook, response.status_code,
        )
        success = False
    except Exception as exc:
        # If an uncaugth exception occured, log and retry
        LOGGER.exception(
            'Delivery failed with exception "%s" for "%s" to %s',
            event['status'], event['id'][:10], hook
        )
        raise self.retry(exc=exc, countdown=countdown)
    else:
        LOGGER.info('Delivered "%s" for "%s" to %s', event['status'],
                    event['id'][:10], hook)
    return {'event': event, 'hook': hook, 'success': success}
