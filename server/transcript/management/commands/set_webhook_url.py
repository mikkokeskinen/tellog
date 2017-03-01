import json

import requests
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.urls import reverse


class Command(BaseCommand):
    help = '''Makes a request to the Telegram API and sets the webhook
            address for the current bot. Bot token is set in the setting
            "TELEGRAM_BOT_TOKEN".

            The full URL will be https://[domain]{path}'''.format(
        path=reverse('transcript:record_telegram'))

    def add_arguments(self, parser):
        parser.add_argument('domain', type=str, )

    def handle(self, *args, **options):
        if not hasattr(settings, 'TELEGRAM_BOT_TOKEN') or \
                not settings.TELEGRAM_BOT_TOKEN:
            raise CommandError('Please set TELEGRAM_BOT_TOKEN setting')

        api_url = 'https://api.telegram.org/bot{token}/setWebhook'.format(
            token=settings.TELEGRAM_BOT_TOKEN)

        payload = {
            'url': 'https://{domain}{path}'.format(
                domain=options['domain'],
                path=reverse('transcript:record_telegram'))
        }

        r = requests.post(api_url, data=payload)

        result_data = r.json()

        if result_data.get('ok'):
            self.stdout.write(self.style.SUCCESS('Success'))
        else:
            self.stdout.write(self.style.ERROR('Failed'))

        if result_data.get('description'):
            self.stdout.write(result_data.get('description'))
