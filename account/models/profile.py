from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxLengthValidator
from account.helper.enums import GenderStatus


from account.repository.manager import ProfileDataAccessLayerManager
from painless.models import (
    TimeStampMixin,
    TruncateMixin
)


class Profile(TimeStampMixin, TruncateMixin):
    """
    User Profile model for extra information
    """

    gender = models.CharField(
        _('gender'),
        max_length=10,
        choices=GenderStatus.choices,
        null=True,
        help_text=_("users' gender")
    )

    nickname = models.CharField(
        _('nick name'),
        max_length=10,
        validators=[MaxLengthValidator(10)],
        null=True,
        help_text=_("nick name")
    )
    job = models.CharField(
        _('job'),
        max_length=30,
        validators=[MaxLengthValidator(30)],
        null=True,
        help_text=_("user's job name")
    )
    birth_date = models.DateField(
        _("birth_date"),
        null=True,
        help_text=_ ("user's birth date")
    )
    national_code = models.CharField(
        _('national code'),
        max_length=10,
        validators=[MaxLengthValidator(10)],
        null=True,
        blank=True,
        help_text=_('National ID.')
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        related_name='profile',
        on_delete=models.PROTECT,
        help_text=_('The user this profile belongs to.')
    )
    is_complete = models.BooleanField(
        _('complete'),
        default=False,
        null=True,
        help_text=_(" weather user's profile is complete")
    )

    dal = ProfileDataAccessLayerManager()
    objects = models.Manager()

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return self.user.phone_number

    def __repr__(self):
        return self.user.phone_number
