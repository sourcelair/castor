import mock
from django.test import TestCase

from docker_events import tasks
from docker_events.models import DockerEvent
from docker_servers.models import DockerServer
from webhooks.models import Delivery
from webhooks.models import WebHook


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
        self.event = {
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
        self.docker_server = DockerServer.objects.create(
            name='localhost',
            docker_host='unix:///var/run/docker.sock',
            docker_tls_verify=False,
            docker_cert_path=None
        )
        self.docker_event = DockerEvent.objects.create(
            docker_server=self.docker_server,
            data=self.event
        )
        self.webhook = WebHook.objects.create(
            docker_server=self.docker_server,
            payload_url='http://localhost'
        )
        def tearDown(self):
            self.docker_event.delete()
            self.webhook.delete()
            self.docker_server.delete()

    def test_successful_event_dispatching(self):
        """
        Ensure that when an event is being dispatched the right requests.post
        call is being made and that the right Delivery object is being created.
        """
        dummy_response = DummyResponse()
        with mock.patch('docker_events.tasks.requests') as requests_mock:
            requests_mock.post.return_value = dummy_response
            tasks.dispatch_docker_event(self.docker_event.id)

        delivery = Delivery.objects.get(
            docker_event=self.docker_event,
            webhook=self.webhook
        )

        requests_mock.post.assert_called_once_with(
            url=self.webhook.payload_url,
            json={
                'event': self.docker_event.data,
                'capture_time': int(self.docker_event.capture_time.timestamp())
            }
        )

        self.assertTrue(delivery.delivered)
        self.assertEqual(delivery.status_code, dummy_response.status_code)
        self.assertEqual(
            delivery.request_headers, dummy_response.request.headers
        )
        self.assertEqual(
            delivery.request_body, dummy_response.request.body
        )
        self.assertEqual(delivery.response_headers, dummy_response.headers)
        self.assertEqual(delivery.response_body, dummy_response.text)

    def test_unsuccessful_event_dispatching(self):
        """
        Ensure that when an event does not get dispatched successfully, the
        appropriate Delivery object is being created
        """
        dummy_exception = Exception('Things went wrong!')

        with mock.patch('docker_events.tasks.requests') as requests_mock:
            requests_mock.post.side_effect = dummy_exception
            tasks.dispatch_docker_event(self.docker_event.id)

        delivery = Delivery.objects.get(
            docker_event=self.docker_event,
            webhook=self.webhook
        )

        self.assertFalse(delivery.delivered)
        self.assertEqual(delivery.failure_reason, str(dummy_exception))
        self.assertEqual(delivery.delivery_duration, 0)
        self.assertEqual(delivery.request_headers, None)
        self.assertEqual(delivery.request_body, None)
        self.assertEqual(delivery.response_headers, None)
        self.assertEqual(delivery.response_body, None)
