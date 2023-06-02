import logging

from django.core.management.base import BaseCommand
from django.apps import apps
from decouple import config

from account.repository.generator_layer import UserDataGenerator

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Demo User
    creates a superuser for demonstration.
    """
    help = 'Generate demo superuser for Account APP.'

    def handle(self, *args, **kwargs):
        logger.debug('Prepare to create demo superuser  ...')
        User = apps.get_model('account', 'User')
        if not User.objects.filter(phone_number=config('BASE_USER_PHONE_NUMBER')).exists():  # noqa
            UserDataGenerator.create_demo_user()
            self.stdout.write(self.style.SUCCESS('Superuser created using given values from settings.ini'))  # noqa
        else:
            self.stdout.write(self.style.ERROR(
                f'Username {config("BASE_USER_PHONE_NUMBER")} already exists.'))
