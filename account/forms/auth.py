import logging

from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import(
    get_user_model,
    authenticate
)

from painless.middlewares import get_request_ip


User = get_user_model()
logger = logging.getLogger('main')


class CustomRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': _('Email')})
        self.fields['phone_number'].widget.attrs.update({'required': 'required', 'placeholder': _('Phone Number')})
        self.fields['password'].widget.attrs.update({'required': 'required', 'placeholder': _('Password')})
        self.fields['confirm_password'].widget.attrs.update({'required': 'required', 'placeholder': _('Confirm Password')})

        if 'data' in kwargs:
            self.request = kwargs['data'].pop('request')[0]

    class Meta:
        model = User
        fields = (
            'email',
            'phone_number',
            'password'
        )
        widgets = {
            'password': forms.PasswordInput(render_value=False),
        }

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password is not None and password != confirm_password:
            self.add_error("confirm_password", "Your passwords must match")

        if password:
            try:
                validate_password(password)
            except ValidationError as e:
                self.add_error('password', e)

        self._post_clean()
        logger.debug(f'Registration failed for:{[*self.errors.keys()]} by {self.data.get("phone_number")}')

        return cleaned_data

    def validate_unique(self):
        exclude = self._get_validation_exclusions()

        try:
            self.instance.validate_unique(exclude=exclude)

        except ValidationError as e:
            logger.info(
                f'{self.data.get("phone_number")} tried to register again with ip address {get_request_ip(self.request)}')
            self._update_errors(e)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            logger.info(f'{self.data.get("phone_number")} has been registered')

        return user


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({"class": "form-control", 'placeholder': _('Phone Number'),})
        self.fields['password'].widget.attrs.update({"class": "form-control", 'placeholder': _('Password')})

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)

            if self.user_cache is None:
                logger.warning(f'{self.data.get("username")} with ip of {get_request_ip(self.request)} failed to log in because of invalid password or username')
                raise self.get_invalid_login_error()

            elif not self.user_cache.is_active:
                logger.warning(f'{self.data.get("username")} with ip of {get_request_ip(self.request)} failed to log in because of not being an ACTIVE user')
                raise self.get_invalid_login_error()

            else:
                self.confirm_login_allowed(self.user_cache)

            logger.info(f'{self.data.get("username")} logged in successfully')

        return self.cleaned_data
