import json
import os


with open('settings.json') as SETTINGS_FILE:
    SETTINGS = json.loads(SETTINGS_FILE.read())
    LOCAL = SETTINGS # Prettier alias

HOOKS = LOCAL.get('hooks', []) # Set up hooks to receive Docker events

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
REDIS_DB = int(os.getenv('REDIS_DB', '1'))
REDIS_URL = os.getenv(
    'REDIS_URL', 'redis://{host}:{port}/{db}'.format(
        host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB,
    )
)

QUEUES = ['castor']

RETRY_POLICY = LOCAL.get('retry_policy', [1, 5, 10, 30, 60])
