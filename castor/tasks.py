from celery import Celery
from settings import SETTINGS
import pickle
import requests


HOOKS = SETTINGS.get('hooks', [])
CELERY_SETTINGS = SETTINGS.get('celery', {})

app = Celery()
app.conf.update(**CELERY_SETTINGS)


@app.task
def dispatch_event(event):
    event_repr = '%s:%s' % (event['id'][:10], event['status'])
    for url in HOOKS:
        dispatch_tuple = (event_repr, url)
        print '[DISPATCH START] Dispatching event %s --> %s' % dispatch_tuple
        try:
            response = requests.post(url, data=event)
            response_tuple = (response.status_code, response.reason)

            if response.status_code >= 400:
                print '  [FAILURE] %s: %s' % response_tuple
            else:
                print '  [SUCCESS] %s: %s' % response_tuple
        except Exception as e:
            print '  [ERROR] Exception: %s' % e
        print '[DISPATCH END] %s --> %s' % dispatch_tuple
    return event


def get_last_event():
    last_event = None
    sql_alchemy_session = dispatch_event.backend.ResultSession()
    query = 'SELECT result from celery_taskmeta ORDER BY date_done DESC LIMIT 1;'
    cursor = sql_alchemy_session.execute(query)
    result = cursor.fetchone()
    sql_alchemy_session.close()

    if result:
        last_event = pickle.loads(result[0])

    return last_event
