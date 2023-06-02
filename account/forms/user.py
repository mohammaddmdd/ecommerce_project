from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserChangeForm,
    UserCreationForm
)

from .fields import PhoneNumberField


User = get_user_model()


class UserChangeExtendedForm(UserChangeForm):
    class Meta:
        field_classes = {"phone_number": PhoneNumberField}


class UserCreationExtendedForm(UserCreationForm):
    phone_number = forms.CharField(
        label=_("Phone Number"),
        strip=False,
        help_text=_("User Phone Number"),
    )
    class Meta:
        model = User
        fields = ("phone_number",)
        field_classes = {"phone_number": PhoneNumberField}