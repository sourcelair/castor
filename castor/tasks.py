from settings import SETTINGS
import requests


HOOKS = SETTINGS.get('hooks', [])


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
