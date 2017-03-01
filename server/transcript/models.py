import json
import datetime

import pytz
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.forms.models import model_to_dict

TELEGRAM_CHAT_TYPE_PRIVATE = 'private'
TELEGRAM_CHAT_TYPE_GROUP = 'group'
TELEGRAM_CHAT_TYPE_SUPERGROUP = 'supergroup'
TELEGRAM_CHAT_TYPE_CHANNEL = 'channel'

TELEGRAM_CHAT_TYPES = (
    (TELEGRAM_CHAT_TYPE_PRIVATE, _('Private')),
    (TELEGRAM_CHAT_TYPE_GROUP, _('Group')),
    (TELEGRAM_CHAT_TYPE_SUPERGROUP, _('Supergroup')),
    (TELEGRAM_CHAT_TYPE_CHANNEL, _('Channel')),
)


class MessageManager(models.Manager):
    def initialize_from_api_data(self, data):
        msgdata = data.get('message', {})

        if not msgdata:
            msgdata = data.get('edited_message', {})

        if not msgdata:
            msgdata = data.get('channel_post', {})

        if not msgdata:
            msgdata = data.get('edited_channel_post', {})

        message = self.model()
        message.update_id = data.get('update_id')
        message.chat_id = msgdata.get('chat', {}).get('id')
        message.chat_type = msgdata.get('chat', {}).get('type')
        if message.chat_type in [TELEGRAM_CHAT_TYPE_GROUP,
                                 TELEGRAM_CHAT_TYPE_SUPERGROUP,
                                 TELEGRAM_CHAT_TYPE_CHANNEL]:
            message.chat_name = msgdata.get('chat', {}).get('title')

        if not message.chat_name and msgdata.get('chat', {}).get('username'):
            message.chat_name = '@{}'.format(
                msgdata.get('chat', {}).get('username'))

        message.message_id = msgdata.get('message_id')
        message.date = datetime.datetime.utcfromtimestamp(
            msgdata.get('date')).replace(tzinfo=pytz.utc)
        if 'edit_date' in msgdata:
            message.edit_date = datetime.datetime.utcfromtimestamp(
                msgdata.get('edit_date')).replace(tzinfo=pytz.utc)
        message.from_username = msgdata.get('from', {}).get('username')
        message.text = msgdata.get('text')
        message.original_data = json.dumps(data)

        return message


class Message(models.Model):
    update_id = models.IntegerField(unique=True)
    chat_id = models.BigIntegerField()
    chat_type = models.CharField(max_length=255, choices=TELEGRAM_CHAT_TYPES)
    chat_name = models.CharField(max_length=4096)
    message_id = models.IntegerField()
    date = models.DateTimeField()
    edit_date = models.DateTimeField(null=True, blank=True)
    obsolete = models.BooleanField(default=False)
    from_username = models.CharField(max_length=32, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    original_data = models.TextField()

    objects = MessageManager()

    def as_dict(self):
        return model_to_dict(self, exclude=['original_data'])
