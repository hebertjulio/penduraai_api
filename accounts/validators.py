from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import Profile


class ProfileBelongUserValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        user = request.user
        qs = user.userprofiles.filter(id=value.id)
        if not qs.exists():
            message = _('This profile does not belong to you.')
            raise serializers.ValidationError(message)


class ProfileOwnerRoleValidator:

    def __call__(self, value):
        if value == Profile.ROLE.owner:
            message = _('Owner role isn\'t allowed.')
            raise serializers.ValidationError(message)
