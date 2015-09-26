"""
Ensure that settings.py gets the proper settings value from settings.json and
the environment.
"""

import mock
import os
import unittest


class EnvironmentTest(unittest.TestCase):
    def setUp(self):
        # Delete settings.pyc in case it exists, since we want the file
        # re-compiled every time that the test suite is being run.
        if os.path.exists('settings.pyc'):
            os.unlink('settings.pyc')

        # Create a settings.json file with empty JSON data
        with open('settings.json', 'w+') as settings_file:
            settings_file.write('{}')

    def tearDown(self):
        os.unlink('settings.json')

    def test_redis_settings(self):
        """
        Ensure that settings are being determined properly when the environment
        variables are available.
        """
        def _mock_getenv(key, default):
            env = {
                'REDIS_HOST': 'redishost',
                'REDIS_PORT': '1234',
                'REDIS_DB': '2'
            }
            return env.get(key, default)

        with mock.patch('os.getenv', new=_mock_getenv):
            from castor import settings

            self.assertEqual(settings.REDIS_HOST, 'redishost')
            self.assertEqual(settings.REDIS_PORT, 1234)
            self.assertEqual(settings.REDIS_DB, 2)
            self.assertEqual(
                settings.REDIS_URL, 'redis://redishost:1234/2'
            )
