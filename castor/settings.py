import json


with open('settings.json') as SETTINGS_FILE:
    SETTINGS = json.loads(SETTINGS_FILE.read())
