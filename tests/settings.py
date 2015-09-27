"""
Ensure that settings.py gets the proper settings value from settings.json and
the environment.
"""

from base import BaseCastorTest
import mock


class BaseSettingsTest(BaseCastorTest):

    def _import_settings(self):
        from castor import settings

        settings = reload(settings)
        return settings


class EnvironmentTest(BaseSettingsTest):
    settings_json_contents = '{}'

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
            settings = self._import_settings()

            self.assertEqual(settings.REDIS_HOST, 'redishost')
            self.assertEqual(settings.REDIS_PORT, 1234)
            self.assertEqual(settings.REDIS_DB, 2)
            self.assertEqual(
                settings.REDIS_URL, 'redis://redishost:1234/2'
            )

class SettingsJSONTest(BaseSettingsTest):
    """
    Tests ensuring the proper parsing of settings.json and storing of its
    data in settings.py.
    """
    settings_json_contents = """
    {
        "hooks": [
            "http://myhost/api/hooks/docker/events"
        ],
        "docker": {
            "base_url": "unix://var/run/docker.sock",
            "version": "1.19"
        }
    }
    """

    def test_hooks(self):
        settings = self._import_settings()

        self.assertEqual(
            settings.HOOKS, ['http://myhost/api/hooks/docker/events']
        )
