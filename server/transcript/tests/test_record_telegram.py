from django.test import TestCase
from django.urls import reverse

from transcript.models import Message


class RecordTelegramTest(TestCase):
    def setUp(self):
        pass

    def test_receive_telegram_POST(self):
        """Test that the transcript recorder accepts the JSON Telegram API
        sends and saves it to the database."""

        response = self.client.post(
            reverse('transcript:record_telegram'),
            content_type='application/json',
            data='''
            {
                "update_id":10000,
                "message":{
                    "date":1441645532,
                    "chat":{
                        "last_name":"Test Lastname",
                        "id":1111111,
                        "type": "private",
                        "first_name":"Test",
                        "username":"Test"
                    },
                    "message_id":1365,
                    "from":{
                        "last_name":"Test Lastname",
                        "id":1111111,
                        "first_name":"Test",
                        "username":"Test"
                    },
                    "text":"/start"
                }
            }''')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"OK")
        self.assertEqual(Message.objects.count(), 1)

    def test_invalid_JSON_returns_error(self):
        """Test that the transcript recorder returns an error if it receives
        invalid JSON."""

        response = self.client.post(
            reverse('transcript:record_telegram'),
            content_type='application/json',
            data='''{"something":''')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Could not parse JSON")
        self.assertEqual(Message.objects.count(), 0)

