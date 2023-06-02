from django.test import TestCase
from django.test.utils import override_settings

from account.models import (
    User,
    Profile,
)


@override_settings(LANGUAGE_CODE='en')
class ProfileModel(TestCase):
    """
    Test Profile-Model that should work properly
    ------

    - testing the magic methods : `__str__` and `__repr__`
    - testing `verbose_name` (single & plural)
    """
    @classmethod
    def setUpClass(cls):
        super(ProfileModel, cls).setUpClass()

        cls.user_one = User.objects.create(
            phone_number='+7-(963)-409-11-22'[:14],
            email='example@gmail.com',
            first_name='Mahmoud',
            last_name='Ahmadinejad',
            # date_joined=cls.get_random_time(),
            is_active=True,
            is_staff=False,
            is_superuser=False,
            password=1
        )

        cls.user_two = User.objects.create(
            phone_number='+7-(963)-500-11-22'[:14],
            email='example2@gmail.com',
            first_name='ahmad',
            last_name='zoghi',
            # date_joined=cls.get_random_time(),
            is_active=True,
            is_staff=False,
            is_superuser=False,
            password=1
        )

        cls.profile_one = Profile.objects.get(
            user=cls.user_one.id,
        )

        cls.profile_two = Profile.objects.get(
            user=cls.user_two.id,
        )

    def test_str_method(self):
        """testing str method in profile Model"""

        actual = str(self.user_one.phone_number)
        expected = self.profile_one.user.phone_number
        self.assertEqual(
            actual,
            expected,
            msg=f"Actual __str__ method is `{actual}` "
            f"but expected is `{expected}`"
        )

    def test_repr_method(self):
        """testing repr method in profile Model"""

        actual = [self.profile_one, self.profile_two]
        expected = list(Profile.objects.all())
        self.assertEqual(
            actual,
            expected,
            msg=f"Actual __repr__ method is `{actual}` "
            f"but expected is `{expected}`"
        )

    def test_verbose_name(self):
        """testing verbose name in profile Model"""

        actual = Profile._meta.verbose_name
        expected = 'Profile'
        self.assertEqual(
            actual,
            expected,
            msg=f"Actual verbose_name is `{actual}` "
            f"but expected is `{expected}`"
        )

        actual = Profile._meta.verbose_name_plural
        expected = 'Profiles'
        self.assertEqual(
            actual,
            expected,
            msg=f"Actual verbose_name_plural is `{actual}` "
            f"but expected is `{expected}`"
        )
