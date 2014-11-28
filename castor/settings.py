import json


SETTINGS_FILE = open('settings.json')
SETTINGS = json.loads(SETTINGS_FILE.read())
SETTINGS_FILE.close()  # We don't have to keep the file open anymore
