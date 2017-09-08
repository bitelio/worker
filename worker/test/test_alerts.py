from unittest import TestCase
from unittest.mock import patch
from unittest.mock import MagicMock

from worker import alerts


credentials = {'APIKEY': 'X', 'SENDER': 's@x.com', 'RECEIVER': 'r@x.com'}


class AlertsTest(TestCase):
    def test_does_nothing(self):
        alert = alerts.SendGrid()
        alert.log.info = MagicMock()
        alert.send('', '')
        alert.log.info.assert_not_called()

    @patch('worker.alerts.SendGrid.post')
    @patch('worker.config.SENDGRID', credentials)
    def test_send(self, post_mock):
        response = MagicMock()
        response.status_code = 200
        post_mock.return_value = response
        traceback = MagicMock()
        traceback.format_exc.return_value = ''
        alert = alerts.SendGrid()
        alert.log.info = MagicMock()
        alert.send('', traceback)
        message = f'Sent email alert to {alert.receiver}'
        alert.log.info.assert_called_once_with(message)
