import logging

from django.utils.text import slugify  # noqa

from tqdm import tqdm

from painless.repository.base import BaseDataGenerator
from account.models import (User,
                            Profile, )

logger = logging.getLogger(__name__)


class AccountDataGenerator(BaseDataGenerator):
    """
    Generates mock data for account.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_user(self, total, batch_size=500, disable_progress_bar=True):
        """
        Generates users using fake data.

        PARAMS
        ------
        `total` : int
            The number of Packs to create.
        `batch_size` : int
            The number of objects to be added to the database in a batch.
        """
        phone_number_set = self.get_unique_phone_number_set(total, digits=13)
        objs = (
            User(
                phone_number=phone_number_set.pop(),
                email=self.get_random_email(),
                first_name=self.get_random_first_name(),
                last_name=self.get_random_last_name(),
                # date_joined=self.get_random_time(),
                is_active=self.get_random_boolean(),
                is_staff=False,
                is_superuser=False,
                password=1,
            ) for _ in tqdm(range(total), disable=disable_progress_bar)
        )
        users = User.objects.bulk_create(objs=objs, batch_size=batch_size)
        logger.debug(f'{total} User objects created successfully.')
        users = User.objects.all()
        return users

    def create_profile(self, batch_size=500, disable_progress_bar=False):
        """
        Generates user profile using fake data, one for each user.

        PARAMS
        ------
        `batch_size` : int
            The number of objects to be added to the database in a batch.
        """
        users = tuple(User.objects.
                      difference(User.objects.filter(profile__isnull=False)))
        objs = (
            Profile(
                user=user,
                national_code=self.get_random_number(1000000000, 9999999999),
                nickname=self.get_random_first_name()[:10],
                job=self.get_random_job(),
                is_complete=self.get_random_boolean(),
                gender=self.get_random_gender(),
                birth_date=self.get_random_datetime(1980,2022),
            ) for user in tqdm(users, disable=disable_progress_bar)
        )
        profiles = Profile.objects.bulk_create(objs=objs, batch_size=batch_size)
        profiles = Profile.objects.all()
        return profiles
