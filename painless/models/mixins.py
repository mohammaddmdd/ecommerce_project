"""
This module contains a collection of mixin classes that can be used to add common functionality to
Django models. Mixins are a way to reuse code in multiple models by creating reusable pieces of 
functionality that can be easily added to any model. Each mixin class in this module provides 
a specific set of functionality that can be added to a model by including it as a parent class.

Examples of functionality provided by these mixins include 
- timestamps, 
- user tracking, 
- image uploading.

By using mixins, developers can easily add common functionality to their models without having to 
repeat the same code in multiple places.
"""
import secrets

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django_countries.fields import CountryField
from django.db import (
    models,
    connection
)
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator
)

from ckeditor_uploader.fields import RichTextUploadingField
from djmoney.models.fields import MoneyField
from khayyam import JalaliDatetime
from sorl.thumbnail import (
    ImageField,
    get_thumbnail
)

from kernel.settings.packages import DEFAULT_CURRENCY_SHOW_ON_SITE
from painless.helper.typing import Dimension


class SKUMixin(models.Model):
    """This model provides a mixin for adding a unique stock unit field (SKU) to other models.

    Attributes:
    sku (CharField): A unique identifier for the object. 
                    It is generated using a secure token and can't be edited.
    """
    sku = models.CharField(
        _('sku'),
        max_length=50,
        validators=[MaxLengthValidator(50)],
        unique=True,
        editable=False,
        default=secrets.token_urlsafe,
        help_text=_('An alternate field to store the unique identity per '
                    'object. This field is also shown in the URL.')
    )

    @admin.display(description=_('stock unit'), ordering=('-sku'))
    def get_sku(self):
        """Returns the first 8 characters of the sku and add '...' at the end."""
        return self.sku[:8] + '...'

    class Meta:
        """The Meta class of the SKUMixin has an attribute abstract = True, 
        making it an abstract class and the fields defined in it will be used in the child classes. 
        The Meta class does not have any other attributes.
        """
        abstract = True


class TitleSlugMixin(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically change help text
        self.__class__.title.field.help_text = _('{0} title.'.format(self.__class__.__name__))  # noqa

    title = models.CharField(
        _('title'),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(
        _('slug'),
        max_length=255,
        unique=True,
        editable=False,
        allow_unicode=True,
        help_text=_('Slug is a newspaper term. A short label for '
                    'something containing only letters, numbers, underscores, '
                    'or hyphens. They are generally used in URLs.')
    )

    @admin.display(description=_('title'), ordering=('-title'))
    def get_title(self):
        return self.title if len(self.title) < 30 else (self.title[:30] + '...')

    class Meta:
        """The Meta class of the TitleSlugMixin has an attribute abstract = True, 
        making it an abstract class and the fields defined in it will be used in the child classes. 
        The Meta class does not have any other attributes.
        """
        abstract = True


class TitleSlugDescriptionMixin(TitleSlugMixin):
    """This model provides a mixin for adding title, slug and description fields to other models. 
    It inherits from TitleSlugMixin and adds a new field for description.

    Attributes:
        title (CharField): The title of the object.
        slug (SlugField): The unique identifier of the object.
        description (RichTextUploadingField): Long description of the object.
    """
    description = RichTextUploadingField(
        _('description'),
        help_text=_('Long description.')
    )

    @admin.display(description=_('title'), ordering=('-title'))
    def get_title(self):
        """Returns the title of the object. If the title is more than 30 characters, 
            it will be truncated to 30 characters and '...' will be added at the end.
        """
        return self.title if len(self.title) < 30 else (self.title[:30] + '...')

    class Meta:
        """The Meta class of the TitleSlugDescriptionMixin has an attribute abstract = True, 
        making it an abstract class and the fields defined in it will be used in the child classes. 
        The Meta class does not have any other attributes.
        """
        abstract = True


class TimeStampMixin(models.Model):
    """This model provides a mixin for adding timestamp fields to other models.
    It automatically records the creation and modification time of records in the database.

    Attributes:
        created (DateTimeField): The time when the record was created in the database.
        modified (DateTimeField): The time when the record was last modified in the database.
    """
    created = models.DateTimeField(
        _('created'),
        auto_now_add=True,
        help_text=_('Automatic registration of record creation time '
                    'in the database.')
    )
    modified = models.DateTimeField(
        _('modified'),
        auto_now=True,
        help_text=_('Automatic registration of record modification time '
                    'in the database.')
    )

    @admin.display(description=_('created'), ordering=('-created'))
    def get_gregorian_created(self):
        """Returns the gregorian creation time of the record in the format '%Y-%m-%d'."""
        return self.created.strftime('%Y-%m-%d')

    @admin.display(description=_('modified'), ordering=('-modified'))
    def get_gregorian_modified(self):
        """Returns the gregorian modification time of the record in the format '%Y-%m-%d'."""
        return self.modified.strftime('%Y-%m-%d')

    @admin.display(description=_('created'), ordering=('-created'))
    def get_solar_created(self):
        """Returns the solar creation time of the record in the format '%d %B %Y'."""
        return JalaliDatetime(self.created).strftime('%d %B %Y')

    @admin.display(description=_('modified'), ordering=('-modified'))
    def get_solar_modified(self):
        """Returns the solar modification time of the record in the format '%d %B %Y'."""
        return JalaliDatetime(self.modified).strftime('%d %B %Y')

    class Meta:
        """The Meta class of the TimeStampMixin has an attribute abstract = True, 
        making it an abstract class and the fields defined in it will be used in the child classes. 
        The Meta class does not have any other attributes.
        """
        abstract = True


class UploadBasePictureMixin(models.Model):
    """The UploadBasePictureMixin is an abstract class that defines fields and methods for
        uploading and storing images on a Django model. The class includes the following fields:

    picture: an ImageField that stores the image file. The upload_to parameter specifies the directory where the image will be stored. The width_field and height_field parameters specify the fields that will store the width and height of the image, respectively.
    alternate_text: a CharField that stores a brief description of the image. This field is intended to be used as an alternate text for the image when it cannot be displayed. The field is optional and has a maximum length of 110 characters.
    width_field and height_field: PositiveIntegerFields that store the width and height of the image, respectively. These fields are intended to be used internally and are not meant to be edited by users.
    """
    picture = models.ImageField(
        _('picture'),
        upload_to='not-config',
        width_field='width_field',
        height_field='height_field',
        help_text=_('The picture that is uploaded.')
    )
    alternate_text = models.CharField(
        _('alternate text'),
        max_length=110,
        validators=[
            MaxLengthValidator(110),
            MinLengthValidator(10)],
        null=True,
        help_text=_('Describe the picture that is uploaded. '
                    'Please write a sound description for '
                    'search engine optimization (SEO).')
    )
    width_field = models.PositiveIntegerField(
        _('width field'),
        editable=False,
        null=True,
        help_text=_("The picture's width.")
    )
    height_field = models.PositiveIntegerField(
        _('height field'),
        editable=False,
        null=True,
        help_text=_("The picture's height.")
    )

    class Meta:
        """The Meta class of the UploadBasePictureMixin has an attribute abstract = True, 
        making it an abstract class and the fields defined in it will be used in the child classes. 
        The Meta class does not have any other attributes.
        """
        abstract = True


class UploadNullAblePictureMixin(UploadBasePictureMixin):

    def get_picture_field(self, *args, **kwargs):
        field = models.ImageField(
            _('Picture'),
            max_length=110,
            upload_to=self.upload_path,
            width_field='width_field',
            height_field='height_field',
            validators=[*self.get_validators()],
            help_text=_('The picture that is uploaded.')
        )
        return field

    class Meta:
        """The Meta class of the UploadNullAblePictureMixin has an attribute abstract = True, 
        making it an abstract class and the fields defined in it will be used in the child classes. 
        The Meta class does not have any other attributes.
        """
        abstract = True


class UploadSorlThumbnailPictureMixin(UploadBasePictureMixin):
    picture = ImageField(
        _('picture'),
        width_field='width_field',
        height_field='height_field',
        help_text=_('The picture that is uploaded.')
    )
    is_default = models.BooleanField(
        _('is default'),
        default=False,
        help_text=_('Is this picture default?')
    )

    def get_thumbnail(self, value: Dimension = Dimension('100x100')):
        return get_thumbnail(self.picture,
                             value,
                             crop='center',
                             quality=99)

    class Meta:
        """The Meta class of the UploadSorlThumbnailPictureMixin has an attribute abstract = True, 
        making it an abstract class and the fields defined in it will be used in the child classes. 
        The Meta class does not have any other attributes.
        """
        abstract = True


class CountryProvinceCityMixin(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.__class__.__name__.lower() == 'order':
            self.__class__.country.field.help_text = _('The country where the '
                                                       'user has submitted '
                                                       'his/her order.')
            self.__class__.province.field.help_text = _('The province where the '
                                                        'user has submitted '
                                                        'his/her order.')
            self.__class__.city.field.help_text = _('The city where the '
                                                    'user has submitted '
                                                    'his/her order.')
            self.__class__.postal_address.field.help_text = _('The postal address where the '  # noqa
                                                              'user has submitted '  # noqa
                                                              'his/her order.')
            self.__class__.postal_code.field.help_text = _('The postal code where the '  # noqa
                                                           'user has submitted '  # noqa
                                                           'his/her order.')
            self.__class__.house_number.field.help_text = _('The license plate number of the house '  # noqa
                                                            'where the user wants to receive his/her order.')  # noqa
            self.__class__.building_unit.field.help_text = _('The house unit number '  # noqa
                                                             'where the user wants to receive his/her order.')  # noqa
        elif self.__class__.__name__.lower() == 'address':
            self.__class__.country.field.help_text = _('The registered country for '  # noqa
                                                       'shipping goods.')
            self.__class__.province.field.help_text = _('The registered province for '  # noqa
                                                        'shipping goods.')
            self.__class__.city.field.help_text = _('The registered city for '
                                                    'shipping goods.')
            self.__class__.postal_address.field.help_text = _('The registered postal address for '  # noqa
                                                              'shipping goods.')
            self.__class__.postal_code.field.help_text = _('The registered postal code for '  # noqa
                                                           'shipping goods.')
            self.__class__.house_number.field.help_text = _('The registered house number for '  # noqa
                                                            'shipping goods.')
            self.__class__.building_unit.field.help_text = _('The registered house unit number for '  # noqa
                                                             'shipping goods.')

    country = CountryField(
        _('country'),
    )
    province = models.CharField(
        _('province'),
        max_length=100,
        validators=[MaxLengthValidator(100)],
    )
    city = models.CharField(
        _('city'),
        max_length=100,
        validators=[MaxLengthValidator(100)],
    )
    postal_address = models.TextField(
        _('postal address'),
    )
    postal_code = models.CharField(
        _('postal code'),
        max_length=50,
        validators=[MaxLengthValidator(50)],
    )
    house_number = models.CharField(
        _('house number'),
        max_length=5,
        validators=[MaxLengthValidator(5)],
    )
    building_unit = models.CharField(
        _('building unit'),
        max_length=5,
        validators=[MaxLengthValidator(5)],
    )

    class Meta:
        abstract = True


class CustomerDetailsMixin(models.Model):
    """A Mixin that provides fields for storing customer details and dynamic help text."""

    def __init__(self, *args, **kwargs):
        """Overrides the parent's init method to set dynamic help text for the customer detail fields."""
        super().__init__(*args, **kwargs)
        if self.__class__.__name__.lower() == 'order':
            self.__class__.receiver_first_name.field.help_text = _(
                'The first name of the person who receives the order.')
            self.__class__.receiver_last_name.field.help_text = _(
                'The last name of the person who receives the order.')
            self.__class__.receiver_phone.field.help_text = _(
                'The phone number of the person who receives the order.')
        elif self.__class__.__name__.lower() == 'address':
            self.__class__.receiver_first_name.field.help_text = _(
                "The receiver's first name to receive the goods.")
            self.__class__.receiver_last_name.field.help_text = _(
                "The receiver's last name to receive the goods.")
            self.__class__.receiver_phone_number.field.help_text = _(
                "The receiver's phone number to receive the goods.")

    receiver_first_name = models.CharField(
        _('receiver first name'),
        max_length=50,
        validators=[MaxLengthValidator(50)],
    )
    receiver_last_name = models.CharField(
        _('receiver last name'),
        max_length=50,
        validators=[MaxLengthValidator(50)],
    )
    receiver_phone_number = models.CharField(
        _('receiver phone number'),
        max_length=13,
        validators=[MaxLengthValidator(13)],
    )

    class Meta:
        """The Meta class of the CustomerDetailsMixin has an attribute abstract = True, 
        making it an abstract class and the fields defined in it will be used in the child classes. 
        The Meta class does not have any other attributes.
        """
        abstract = True


class LogisticCostMixin(models.Model):
    """A Mixin that provides a `logistic_cost` field with a dynamic help text."""

    def __init__(self, *args, **kwargs):
        """
        Overrides the parent's init method to set dynamic help text for the logistic_cost field
        """
        super().__init__(*args, **kwargs)

        self.__class__.logistic_cost.field.help_text = \
            _('If the logistic type is {0} based, '
              'it takes the value of the money type.'
              .format((self.__class__.__name__)[8:-5]))

    logistic_cost = MoneyField(
        _('logistic cost'),
        null=True,
        max_digits=14,
        decimal_places=2,
        default_currency=DEFAULT_CURRENCY_SHOW_ON_SITE,
        help_text=_('A field that stores the logistic cost of the model.')
    )

    class Meta:
        """The Meta class of the LogisticCostMixin has an attribute abstract = True, 
        making it an abstract class and the fields defined in it will be used in the child classes. 
        The Meta class does not have any other attributes.
        """
        abstract = True


class TruncateMixin:
    """A Mixin that provides a method to truncate the current model's table."""

    @classmethod
    def truncate(cls):
        """
        Truncates the table associated with the current model.

        This method uses the `connection.cursor()` to execute a TRUNCATE TABLE query 
        on the current model's table. The truncation is done using CASCADE to also truncate 
        any related tables.

        Returns:
            None
        """
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE '{0}' CASCADE".format(cls._meta.db_table))  # noqa


class AdminLoginAttempt(models.Model):
    """This model represents the login attempts for an admin user. 
    It keeps track of the number of times an admin user has successfully logged in, 
    as well as the number of failed login attempts.

    Attributes:
        user (OneToOneField): A one-to-one relationship with the admin user model.
        login_count (IntegerField): The number of times the user has successfully logged in.
        failed_attempts (IntegerField): The number of failed login attempts for the user.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text=_("The admin user associated with this login count.")
    )
    login_count = models.IntegerField(
        default=0,
        help_text=_("The number of times this admin user has successfully logged in.")
    )
    failed_attempts = models.IntegerField(
        default=0,
        help_text=_("The number of failed login attempts for this admin user.")
    )

    class Meta:
        """The Meta class of the AdminLoginAttempt has an attribute abstract = True, 
        making it an abstract class and the fields defined in it will be used in the child classes. 
        The Meta class does not have any other attributes.
        """
        abstract = True
