"""
This module contains tests that assure the proper functioning of Castor tasks.
"""
import celery
import mock
import requests

from base import BaseCastorTest


class TasksTest(BaseCastorTest):
    settings_json_contents = """
    {
        "hooks": [
            "http://myhost/api/hooks/docker/events"
        ],
        "retry_policy": [1, 5, 10]
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
            tasks.dispatch_event(event,
                                 'http://myhost/api/hooks/docker/events')

        post_mock.assert_called_once_with(
            'http://myhost/api/hooks/docker/events', data=event
        )

    def test_dispatch_event_redelivery_server_error(self):
        """
        Ensure that tasks are redelievered in case of a server error.
        """

        from castor import tasks

        event = {
            'id': 'abc',
            'status': 'create',
            'time': 123456,
            'from': 'ubuntu:latest'
        }

        with mock.patch('castor.tasks.requests.post') as post_mock:
            exc = requests.exceptions.HTTPError()
            post_mock.return_value.raise_for_status.side_effect = exc
            post_mock.return_value.status_code = 500
            tasks.dispatch_event.retry = mock.MagicMock(
                side_effect=celery.exceptions.Retry)
            self.assertRaises(
                celery.exceptions.Retry, tasks.dispatch_event,
                event, 'http://myhost/api/hooks/docker/events'
            )

    def test_dispatch_event_redelivery_uncaught_error(self):
        """
        Ensure that tasks are redelievered in case of an uncaught error.
        """

        from castor import tasks

        event = {
            'id': 'abc',
            'status': 'create',
            'time': 123456,
            'from': 'ubuntu:latest'
        }

        with mock.patch('castor.tasks.requests.post') as post_mock:
            post_mock.return_value.raise_for_status.side_effect = Exception()
            tasks.dispatch_event.retry = mock.MagicMock(
                side_effect=celery.exceptions.Retry)
            self.assertRaises(
                celery.exceptions.Retry, tasks.dispatch_event,
                event, 'http://myhost/api/hooks/docker/events'
            )

    def test_dispatch_event_redelivery_declined(self):
        """
        Ensure that tasks are not redelievered in case of a 4XX response.
        """

        from castor import tasks

        event = {
            'id': 'abc',
            'status': 'create',
            'time': 123456,
            'from': 'ubuntu:latest'
        }

        with mock.patch('castor.tasks.requests.post') as post_mock:
            exc = requests.exceptions.HTTPError()
            post_mock.return_value.raise_for_status.side_effect = exc
            post_mock.return_value.status_code = 400
            tasks.dispatch_event(event,
                                 'http://myhost/api/hooks/docker/events')
        post_mock.assert_called_once_with(
            'http://myhost/api/hooks/docker/events', data=event
        )
