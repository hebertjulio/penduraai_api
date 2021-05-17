from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from model_utils.models import TimeStampedModel
from model_utils import Choices


class Record(TimeStampedModel):

    OPERATION = Choices(
        ('credit', _('credit')),
        ('debt', _('debt')),
    )

    id = models.BigAutoField(primary_key=True, editable=False)
    note = models.CharField(('note'), max_length=255, blank=True)

    value = models.DecimalField(
        _('value'), max_digits=10, decimal_places=2,
        validators=[
            MinValueValidator(0.01)
        ]
    )

    operation = models.CharField(
        _('operation'), max_length=30, db_index=True,
        choices=OPERATION
    )

    sheet = models.ForeignKey(
        'Sheet', on_delete=models.CASCADE,
        related_name='sheetrecords',
    )

    attendant = models.ForeignKey(
        'accounts.Profile', on_delete=models.CASCADE,
        related_name='attendantrecords',
    )

    signatary = models.ForeignKey(
        'accounts.Profile', on_delete=models.CASCADE,
        related_name='signataryrecords',
    )

    is_active = models.BooleanField(
        _('active status'),
        default=True,
        help_text=_(
            'Designates whether this record should be treated as active. '
            'Unselect this instead of deleting record.'
        ),
    )

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    def __str__(self):
        return 'Record %s' % self.id

    def __repr__(self):
        return 'Record %s' % self.id

    class Meta:
        verbose_name = _('record')
        verbose_name_plural = _('records')


class Sheet(TimeStampedModel):

    id = models.BigAutoField(primary_key=True, editable=False)

    merchant = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        related_name='merchantsheets',
    )

    customer = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        related_name='customersheets',
    )

    profiles = models.ManyToManyField(
        'accounts.Profile', blank=True, related_name='sheetprofiles'
    )

    is_active = models.BooleanField(
        _('active status'),
        default=True,
        help_text=_(
            'Designates whether this sheet should be treated as active. '
            'Unselect this instead of deleting sheet.'
        ),
    )

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    def __str__(self):
        return 'Sheet %s' % self.id

    def __repr__(self):
        return 'Sheet %s' % self.id

    class Meta:
        verbose_name = _('sheet')
        verbose_name_plural = _('sheets')
        unique_together = [
            ['merchant', 'customer']
        ]
