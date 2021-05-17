from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class UserAlreadyCustomerValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        qs = value.merchantsheets.filter(customer=request.user)
        if qs.exists():
            message = _('You already customer of merchant.')
            raise serializers.ValidationError(message)


class CustomerYourselfValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        if value.id == request.user.id:
            message = _('You cannot be a customer of yourself.')
            raise serializers.ValidationError(message)


class CustomerOfMerchantValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        qs = value.merchantsheets.filter(customer=request.user, is_active=True)
        if not qs.exists():
            message = _('You aren\'t customer of merchant.')
            raise serializers.ValidationError(message)


class ProfileCanBuyValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        profile = request.user.profile
        if not profile.is_owner:
            qs = value.merchantsheets.filter(profiles__id=profile.id)
            if not qs.exists():
                message = _('You cannot buy from this merchant.')
                raise serializers.ValidationError(message)
