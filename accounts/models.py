from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from model_utils.models import TimeStampedModel
from model_utils import Choices

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):

    id = models.BigAutoField(primary_key=True, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('name'), max_length=50)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )

    is_active = models.BooleanField(
        _('active status'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return '%s (%s)' % (self.name, self.id)

    def __repr__(self):
        return '%s (%s)' % (self.name, self.id)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Profile(TimeStampedModel):

    ROLE = Choices(
        ('owner', _('owner')),
        ('manager', _('manager')),
        ('attendant', _('attendant')),
        ('guest', _('guest')),
    )

    PIN_REGEX = r'\d{4}'

    id = models.BigAutoField(primary_key=True, editable=False)
    name = models.CharField(_('name'), max_length=30)

    pin = models.CharField(_('pin'), max_length=4, validators=[
        RegexValidator(PIN_REGEX)
    ], db_index=True)

    user = models.ForeignKey(
        'User', on_delete=models.CASCADE,
        related_name='userprofiles',
    )

    is_active = models.BooleanField(
        _('active status'),
        default=True,
        help_text=_(
            'Designates whether this profile should be treated as active. '
            'Unselect this instead of deleting profile.'
        ),
    )

    role = models.CharField(
        _('role'), max_length=30, db_index=True,
        choices=ROLE
    )

    @property
    def is_owner(self):
        return self.role == self.ROLE.owner

    @property
    def is_manager(self):
        return self.role == self.ROLE.manager

    @property
    def is_attendant(self):
        return self.role == self.ROLE.attendant

    @property
    def is_guest(self):
        return self.role == self.ROLE.guest

    def __str__(self):
        return '%s (%s)' % (self.name, self.id)

    def __repr__(self):
        return '%s (%s)' % (self.name, self.id)

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')
