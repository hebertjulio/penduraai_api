from rest_framework import serializers

from accounts.relations import UserRelatedField, ProfileRelatedField
from accounts.fields import CurrentProfileDefault

from bridges.services import create_transaction

from .relations import SheetRelatedField
from .models import Record, Sheet

from .validators import (
    ProfileCanBuyValidator, CustomerOfMerchantValidator,
    UserAlreadyCustomerValidator, CustomerYourselfValidator
)


class RecordCreateSerializer(serializers.ModelSerializer):

    merchant = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    attendant = serializers.HiddenField(default=CurrentProfileDefault())

    def create(self, validated_data):
        transaction = create_transaction(validated_data, 900, 'record')
        validated_data.update({'transaction': transaction.id})
        return validated_data

    class Meta:
        model = Record
        exclude = [
            'sheet', 'signatary'
        ]


class RecordConfirmSerializer(serializers.ModelSerializer):

    merchant = UserRelatedField(
        validators=[CustomerOfMerchantValidator(), ProfileCanBuyValidator()])

    signatary = serializers.HiddenField(default=CurrentProfileDefault())

    def create(self, validated_data):
        merchant = validated_data.pop('merchant')
        request = self.context['request']
        sheet = merchant.merchantsheets.get(customer=request.user)
        validated_data.update({'sheet': sheet})
        return super().create(validated_data)

    class Meta:
        model = Record
        exclude = [
            'sheet'
        ]


class RecordReadSerializer(serializers.ModelSerializer):

    transaction = serializers.UUIDField(read_only=True)
    sheet = SheetRelatedField(read_only=True)
    attendant = ProfileRelatedField(read_only=True)
    signatary = ProfileRelatedField(read_only=True)

    class Meta:
        model = Record
        read_only_fields = Record.get_fields()
        fields = '__all__'


class SheetCreateSerializer(serializers.ModelSerializer):

    merchant = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    profiles = serializers.HiddenField(default=[])

    def create(self, validated_data):
        transaction = create_transaction(validated_data, 900, 'sheet')
        validated_data.update({'transaction': transaction.id})
        return validated_data

    class Meta:
        model = Sheet
        exclude = [
            'customer'
        ]


class SheetConfirmSerializer(serializers.ModelSerializer):

    merchant = UserRelatedField(
        validators=[
            UserAlreadyCustomerValidator(),
            CustomerYourselfValidator()])

    customer = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Sheet
        fields = '__all__'


class SheetUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sheet
        fields = [
            'is_active'
        ]


class SheetReadSerializer(serializers.ModelSerializer):

    transaction = serializers.UUIDField(read_only=True)
    merchant = UserRelatedField(read_only=True)
    customer = UserRelatedField(read_only=True)

    balance = serializers.DecimalField(
        read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = Sheet
        read_only_fields = Sheet.get_fields()
        fields = '__all__'
