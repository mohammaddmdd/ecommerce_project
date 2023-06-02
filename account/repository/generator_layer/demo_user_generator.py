import logging

from decouple import config

from django.apps import apps

logger = logging.getLogger(__name__)


class UserDataGenerator:
    @staticmethod
    def create_demo_user():
        """
        creates a superuser from BASE_USER in settings.ini for demo purposes.
        """
        User = apps.get_model('account', 'User')
        logger.debug('User objects created successfully.')
        demo_user = User.dal.create_superuser(
            phone_number=config('BASE_USER_PHONE_NUMBER'),
            is_staff=True,
            password=config('BASE_PASSWORD'),
        )
        logger.debug('User are saved into the database.')
        return demo_user
