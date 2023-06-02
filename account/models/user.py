import uuid
from typing import List

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator
)

from account.repository.manager import UserManager
from account.repository.business_layer.manager import AccountBusinessLogicLayer
from painless.helper.enums import RegexPatternEnum
from painless.models import (
    TimeStampMixin,
    TruncateMixin
)


class User(AbstractUser, TimeStampMixin, TruncateMixin):
    """
    Custom-made User class, overriding `username` and changing USERNAME_FIELD
    to phone_number.
    """
    orders_list: List
    username = None
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = list()
    secret = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        help_text=_('A user token for sending emails and OTP verification.')
    )
    first_name = models.CharField(
        _('first name'),
        null=True,
        blank=True,
        max_length=30,
        validators=[MinLengthValidator(3), MaxLengthValidator(30)],
        help_text=_("User's first name.")
    )
    last_name = models.CharField(
        _('last name'),
        null=True,
        blank=True,
        max_length=30,
        validators=[MinLengthValidator(3), MaxLengthValidator(30)],
        help_text=_("User's last name.")
    )
    phone_number = models.CharField(
        _('phone number'),
        max_length=15,
        validators=[RegexValidator(RegexPatternEnum.IRAN_PHONE_NUMBER.value),
                    MaxLengthValidator(15)],
        unique=True,
        help_text=_("User's phone number.")
    )
    email = models.EmailField(
        _('email'),
        null=True,
        blank=True,
        help_text=_("User's email.")
    )

    @property
    def get_cart_slug(self):
        return self.cart.slug

    def get_cart(self):
        return self.cart

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''

    def send_otp(self, subject, message, from_number, **kwargs):
        '''
        Sends an sms to this User
        '''
        ...
    dal = UserManager()
    bll = AccountBusinessLogicLayer()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return f'{self.phone_number}'

    def __repr__(self):
        return f'{self.phone_number}'
