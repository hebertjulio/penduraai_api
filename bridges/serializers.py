from rest_framework import serializers

from .models import Transaction


class TransactionReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        read_only_fields = Transaction.get_fields()
        fields = '__all__'
