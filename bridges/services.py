from datetime import timedelta
from json import dumps

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Model
from django.utils import timezone

from .models import Transaction
from .encoders import DecimalEncoder


def create_transaction(data, expire, scope):
    now = timezone.now()
    expire_in = now + timedelta(seconds=expire)
    data = dumps({
        k: v.id if isinstance(v, Model) else v
        for k, v in data.items()
    }, cls=DecimalEncoder)
    transaction = Transaction.objects.create(
        scope=scope, expire_in=expire_in,
        data=data
    )
    return transaction


def send_ws_message(group, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group, {
            'type': 'websocket.send',
            'text': message,
        },
    )
