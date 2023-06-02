from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin

from jalali_date.admin import ModelAdminJalaliMixin

from account.forms import (
    UserChangeExtendedForm,
    UserCreationExtendedForm
)
from account.models import (
    User,
    Profile
)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


@admin.register(User)
class CustomUserAdmin(ModelAdminJalaliMixin, UserAdmin):
    add_form = UserCreationExtendedForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "password1", "password2"),
            },
        ),
    )

    list_display = (
        'phone_number',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'is_superuser',
        'last_login',
    )

    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
        'last_login',
        'date_joined',
    )

    search_fields = (
        'first_name',
        'last_name',
        'phone_number',
    )
    
    ordering = (
        'phone_number',
    )

    search_help_text = 'you can look for user by first_name,last_name, username, phone_number' # noqa

    save_on_top = True

    readonly_fields = (
        'username',
    )

    inlines = (
        ProfileInline, 
    )

