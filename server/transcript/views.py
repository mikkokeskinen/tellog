import json

import voluptuous
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import SearchForm
from .models import Message
from .telegram_schema import telegram_schema
from .serializers import TellogJSONEncoder


@require_POST
@csrf_exempt
def record_telegram(request):
    if request.content_type != 'application/json':
        return HttpResponseBadRequest("Content type application/json required")

    body_unicode = request.body.decode('utf-8')

    try:
        data = json.loads(body_unicode)
    except json.JSONDecodeError as e:
        return HttpResponseBadRequest("Could not parse JSON")

    # Validate the received data
    try:
        data = telegram_schema(data)
    except voluptuous.error.Invalid:
        return HttpResponseBadRequest("Data not valid")

    message = Message.objects.initialize_from_api_data(data)

    if message.edit_date:
        # As we keep all versions of edited messages, mark older entries as
        # obsolete
        Message.objects.filter(chat_id=message.chat_id,
                               message_id=message.message_id).update(
            obsolete=True)

    message.save()

    return HttpResponse("OK")


def message_search(request):
    errors = []
    form = SearchForm(request.GET)

    if form.is_valid():
        messages = Message.objects.filter(text__isnull=False,
                                          obsolete=False).order_by('date')

        if form.cleaned_data['q']:
            messages = messages.filter(text__search=form.cleaned_data['q'])

        if form.cleaned_data['username']:
            messages = messages.filter(
                from_username=form.cleaned_data['username'])

        if form.cleaned_data['date']:
            messages = messages.filter(date__date=form.cleaned_data['date'])

        return JsonResponse({
            'success': True,
            'messages': list(messages),
        }, encoder=TellogJSONEncoder)

    else:
        for key, error in form.errors.items():
            errors.append(error)

    return JsonResponse({
        'success': False,
        'errors': errors,
    })
