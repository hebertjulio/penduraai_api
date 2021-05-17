from rest_framework.exceptions import NotFound
from rest_framework import generics

from rest_framework_api_key.permissions import HasAPIKey

from .serializers import TransactionReadSerializer
from .models import Transaction
from .services import send_ws_message


class TransactionDetailView(generics.RetrieveDestroyAPIView):

    serializer_class = TransactionReadSerializer
    lookup_url_kwarg = 'transaction_id'

    permission_classes = [
        HasAPIKey
    ]

    def get_object(self):
        try:
            transaction_id = self.kwargs[self.lookup_url_kwarg]
            transaction = Transaction.objects.get(pk=transaction_id)
            return transaction
        except Transaction.DoesNotExist:
            raise NotFound

    def perform_destroy(self, instance):
        instance.usage = -1
        instance.save()
        send_ws_message(instance.id, 'REJECTED')
