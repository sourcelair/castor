from unittest import mock
from django.test import TestCase

from docker_servers.models import DockerServer
from webhooks.models import WebHook
from webhooks import tasks


DUMMY_EVENT = {
    'id': 'f8b07d4d79',
    'Type': 'container',
    'from': 'castor_web',
    'time': 1485336358,
    'Actor': {
        'ID': 'f8b07d4d79',
        'Attributes': {
            'name': "castor_web_1",
            'image': "castor_web",
            'exitCode': "137",
            'com.docker.compose.oneoff': 'False',
            'com.docker.compose.project': 'castor',
            'com.docker.compose.service': 'web',
            'com.docker.compose.version': '1.10.0',
            'com.docker.compose.config-hash': '0a2fe5a497',
            'com.docker.compose.container-number': '1'
        }
    },
    'Action': 'die',
    'status': 'die',
    'timeNano': 1485336358937541198
}


class DummyRequest(object):
    headers = {
        'Request-Header': 'SomeValue'
    }
    body = '{"status": "start"}'


class DummyResponse(object):
    request = DummyRequest()
    status_code = 200
    headers = {
        'Response-Header': 'SomeOtherValue'
    }
    text = 'OK.'


class TasksTestCase(TestCase):
    def setUp(self):
        self.docker_server = DockerServer.objects.create(
            name='localhost',
            docker_host='unix:///var/run/docker.sock',
            docker_tls_verify=False,
            docker_cert_path=None
        )
        self.webhook_1 = WebHook.objects.create(
            docker_server=self.docker_server,
            payload_url='http://localhost'
        )
        self.webhook_2 = WebHook.objects.create(
            docker_server=self.docker_server,
            payload_url='http://localhost.local'
        )

    def tearDown(self):
        self.webhook_1.delete()
        self.webhook_2.delete()
        self.docker_server.delete()

    def test_successful_event_dispatching_to_webhook(self):
        """
        Ensure that when an event is being dispatched to a WebHook, the right
        requests.post call is being made and that the right delivery dict is
        being return.
        """
        dummy_response = DummyResponse()
        with mock.patch('webhooks.tasks.requests') as requests_mock:
            requests_mock.post.return_value = dummy_response
            delivery = tasks.dispatch_docker_event_to_webhook(
                DUMMY_EVENT, self.webhook_1.id
            )

        requests_mock.post.assert_called_once_with(
            url=self.webhook_1.payload_url,
            json={
                'event': DUMMY_EVENT,
                'docker_server': self.webhook_1.docker_server.name
            },
            headers={
                'user-agent': 'Castor/0.1 via python-requests/2.12.5'
            }
        )

        self.assertTrue(delivery['delivered'])
        self.assertEqual(delivery['status_code'], dummy_response.status_code)
        self.assertEqual(
            delivery['request_headers'], dummy_response.request.headers
        )
        self.assertEqual(
            delivery['request_body'], dummy_response.request.body
        )
        self.assertEqual(delivery['response_headers'], dummy_response.headers)
        self.assertEqual(delivery['response_body'], dummy_response.text)

    def test_unsuccessful_event_dispatching_to_webhook(self):
        """
        Ensure that when an event does not get dispatched successfully, the
        appropriate dict is being returned.
        """
        dummy_exception = Exception('Things went wrong!')

        with mock.patch('webhooks.tasks.requests') as requests_mock:
            requests_mock.post.side_effect = dummy_exception
            delivery = tasks.dispatch_docker_event_to_webhook(
                DUMMY_EVENT, self.webhook_1.id
            )

        self.assertFalse(delivery['delivered'])
        self.assertEqual(delivery['failure_reason'], str(dummy_exception))
        self.assertEqual(delivery['delivery_duration'], 0)
        self.assertEqual(delivery['request_headers'], None)
        self.assertEqual(delivery['request_body'], None)
        self.assertEqual(delivery['response_headers'], None)
        self.assertEqual(delivery['response_body'], None)

    def test_dispatching_of_docker_event_to_all_webhooks(self):
        """
        Make sure that every time a Docker event is put for dispatching, that
        it is being dispatched to all WebHooks of the corresponding
        DockerServer.
        """
        with mock.patch(
            'webhooks.tasks.dispatch_docker_event_to_webhook'
        ) as dispatch_mock:
            tasks.dispatch_docker_event(DUMMY_EVENT, self.docker_server.pk)

        dispatch_mock.delay.assert_has_calls(
            [
                mock.call(DUMMY_EVENT, self.webhook_1.id),
                mock.call(DUMMY_EVENT, self.webhook_2.id)
            ],
            any_order=True
        )
