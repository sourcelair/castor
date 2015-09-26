import json
import os


with open('settings.json') as SETTINGS_FILE:
    SETTINGS = json.loads(SETTINGS_FILE.read())
    LOCAL = SETTINGS # Prettier alias

HOOKS = LOCAL.get('hooks', []) # Set up hooks to receive Docker events

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
REDIS_DB = int(os.getenv('REDIS_DB', '1'))
REDIS_URL = os.getenv('REDIS_URL', 'redis://%s:%s/%s' % (
    REDIS_HOST, str(REDIS_PORT), str(REDIS_DB)
))

QUEUES = ['castor']
