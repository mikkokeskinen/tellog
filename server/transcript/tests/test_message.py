import json
import datetime

import pytz
from django.test import TestCase

from transcript.models import Message, TELEGRAM_CHAT_TYPE_PRIVATE


class MessageTest(TestCase):
    def test_initialize_from_api_data(self):
        """Test that the initialize_from_api_data method in MessageManager
        initializes the message data."""

        data = json.loads('''
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

        message = Message.objects.initialize_from_api_data(data)

        self.assertEqual(message.update_id, 10000)
        self.assertEqual(message.chat_id, 1111111)
        self.assertEqual(message.chat_type, TELEGRAM_CHAT_TYPE_PRIVATE)
        self.assertEqual(message.chat_name, '@Test')
        self.assertEqual(message.message_id, 1365)
        self.assertEqual(message.date, datetime.datetime(2015, 9, 7, 17, 5, 32,
                                                         tzinfo=pytz.utc))
        self.assertEqual(message.edit_date, None)
        self.assertEqual(message.obsolete, False)
        self.assertEqual(message.from_username, "Test")
        self.assertEqual(message.text, "/start")
        self.assertEqual(message.original_data, json.dumps(data))
