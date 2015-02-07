"""
This module declares all tasks that dispatch Docker events to the hooks
defined in ``settings.py``.
"""

from celery import Celery
from settings import SETTINGS
import pickle
import requests


HOOKS = SETTINGS.get('hooks', [])
CELERY_SETTINGS = SETTINGS.get('celery', {})

app = Celery()
app.conf.update(**CELERY_SETTINGS)


@app.task
def dispatch_web_hook(url, payload):
    """
    Makes a POST request to the given URL, with the given payload.
    """
    print 'Dispatching payload to %s' % url
    try:
        response = requests.post(url, data=payload)
        response_tuple = (response.status_code, response.reason)
    except Exception as e:
        print '[ERROR] Exception: %s' % e


@app.task
def dispatch_event(event):
    """
    Dispatches the given event to all registered hooks.
    """
    event_repr = '%s:%s' % (event['id'][:10], event['status'])
    for url in HOOKS:
        print 'Dispatching event %s to %s' % (event_repr, url)
        dispatch_web_hook.delay(url, event)
    return event  # We return the event for later querying
