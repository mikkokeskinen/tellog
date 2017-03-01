from django.core.serializers.json import DjangoJSONEncoder

from .models import Message


class TellogJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, Message):
            return o.as_dict()
        else:
            return super(TellogJSONEncoder, self).default(o)
