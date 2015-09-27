"""
This module contains tests that assure the proper functioning of Castor tasks.
"""

from base import BaseCastorTest
import mock


class TasksTest(BaseCastorTest):
    settings_json_contents = """
    {
        "hooks": [
            "http://myhost/api/hooks/docker/events"
        ]
    }
    """

    def test_dispatch_event_to_single_hook(self):
        """
        Ensure that tasks dispatch the proper Docker event to the appropriate
        hook.
        """

        from castor import tasks

        event = {
            'id': 'abc',
            'status': 'create',
            'time': 123456,
            'from': 'ubuntu:latest'
        }

        with mock.patch('castor.tasks.requests.post') as post_mock:
            tasks.dispatch_event(event)

        post_mock.assert_called_once_with(
            'http://myhost/api/hooks/docker/events', data=event
        )
