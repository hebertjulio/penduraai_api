from functools import wraps, partial

from rest_framework.exceptions import ValidationError

from .models import Transaction
from .services import send_ws_message


def use_transaction(func=None, lookup_url_kwarg=None):
    if func is None:
        return partial(use_transaction, lookup_url_kwarg=lookup_url_kwarg)

    @wraps(func)
    def wapper(self, request, *args, **kwargs):
        transaction_id = kwargs[lookup_url_kwarg]
        try:
            self.transaction = Transaction.objects.get(pk=transaction_id)
            self.transaction.expired(raise_exception=True)
            self.transaction.usaged(raise_exception=True)
        except (
                Transaction.DoesNotExist,
                Transaction.Usaged, Transaction.Expired) as e:
            raise ValidationError(detail=str(e))

        result = func(self, request, *args, **kwargs)
        self.transaction.usage += 1
        self.save()
        send_ws_message(transaction_id, 'CONFIRMED')
        return result
    return wapper
