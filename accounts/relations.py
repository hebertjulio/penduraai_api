from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.validators import ValidationError

from .models import User, Profile


class UserRelatedField(serializers.RelatedField):

    def get_object(self, pk):
        try:
            qs = self.get_queryset()
            return qs.get(pk=pk)
        except User.DoesNotExist:
            raise ValidationError(_('User does not exist.'))

    def get_queryset(self):
        if self.read_only:
            return None
        qs = User.objects.all()
        return qs

    def to_internal_value(self, data):
        if isinstance(data, User):
            return data
        return self.get_object(data)

    def to_representation(self, value):
        data = {'id': value.id, 'name': value.name}
        return data


class ProfileRelatedField(serializers.RelatedField):

    def get_object(self, pk):
        try:
            qs = self.get_queryset()
            return qs.get(pk=pk)
        except Profile.DoesNotExist:
            raise ValidationError(_('Profile does not exist.'))

    def get_queryset(self):
        if self.read_only:
            return None
        qs = Profile.objects.all()
        return qs

    def to_internal_value(self, data):
        if isinstance(data, Profile):
            return data
        return self.get_object(data)

    def to_representation(self, value):
        data = {'id': value.id, 'name': value.name}
        return data
