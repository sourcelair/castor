"""
Base Castor test case classes.
"""

import os
import unittest


class BaseCastorTest(unittest.TestCase):
    settings_json_contents = None

    def setUp(self):
        # Delete settings.pyc in case it exists, since we want the file
        # re-compiled every time that the test suite is being run.
        if os.path.exists('settings.pyc'):
            os.unlink('settings.pyc')

        # Create a settings.json file with empty JSON data
        with open('settings.json', 'w+') as settings_file:
            settings_file.write(self.settings_json_contents)

    def tearDown(self):
        # Remove the settings.json file created
        os.unlink('settings.json')
