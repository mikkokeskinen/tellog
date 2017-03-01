import json

from django.test import TestCase
from voluptuous import MultipleInvalid, RequiredFieldInvalid

from transcript.telegram_schema import telegram_schema


class SchemaValidationTest(TestCase):
    def test_valid_data(self):
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

        telegram_schema(data)

    def test_missing_update_id(self):
        data = json.loads('''
            {
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

        with self.assertRaises(MultipleInvalid) as cm:
            telegram_schema(data)

        exception = cm.exception

        self.assertEqual(str(exception),
                         "required key not provided @ data['update_id']")

    def test_extraneous_key(self):
        data = json.loads('''
        {
            "update_id":10000,
            "edited_message":{
                "date":1441645532,
                "chat":{
                     "last_name":"Test Lastname",
                     "type": "private",
                     "id":1111111,
                     "first_name":"Test Firstname",
                     "extra_key":0,
                     "username":"Testusername"
                },
                "message_id":1365,
                "from":{
                    "last_name":"Test Lastname",
                    "id":1111111,
                    "first_name":"Test Firstname",
                    "username":"Testusername"
                },
                "text":"Edited text",
                "edit_date": 1441646600
            }
        }''')

        with self.assertRaises(MultipleInvalid) as cm:
            telegram_schema(data)

        exception = cm.exception

        self.assertEqual(str(exception),
                         "extra keys not allowed @ "
                         "data['edited_message']['chat']['extra_key']")

