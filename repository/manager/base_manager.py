from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from account.repository.queryset import UserQuerySet


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, password, **extra_fields):
        """
        Creates and saves a User with the given phone_number and password.
        """
        if not phone_number:
            raise ValueError('`phone_number` must be set.')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self._create_user(phone_number, password, **extra_fields)

    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def get_normal_users(self):
        return self.get_queryset().get_normal_users()

    def get_actives(self):
        return self.get_queryset().get_actives()

    def get_users_who_made_the_most_number_of_purchases(self):
        return self.get_queryset().get_users_who_made_the_most_number_of_purchases()

    def get_users_to_whom_we_have_sold_the_most(self):
        return self.get_queryset().get_users_to_whom_we_have_sold_the_most()

    def get_users_from_whom_we_have_benefited_the_most(self):
        return self.get_queryset().get_users_from_whom_we_have_benefited_the_most()

    def get_users_who_bought_from_a_specific_brand(self, brand_title: str):
        return self.get_queryset().get_users_who_bought_from_a_specific_brand(brand_title = brand_title)

    def get_users_who_made_discounted_purchases(self):
        return self.get_queryset().get_users_who_made_discounted_purchases()

    def get_users_who_have_not_made_a_purchase_yet(self):
        return self.get_queryset().get_users_who_have_not_made_a_purchase_yet()

    def get_amount_of_refund_request_per_user(self):
        return self.get_queryset().get_amount_of_refund_request_per_user()

    def get_users_who_have_made_several_purchases_of_a_certain_color(self, color_title: str):
        return self.get_queryset().get_users_who_have_made_several_purchases_of_a_certain_color(color_title = color_title)

    def get_total_delivered_or_canceled_order_per_user(self):
        return self.get_queryset().get_total_delivered_or_canceled_order_per_user()

    def get_order_status(self, order_status : str):
        return self.get_queryset().get_order_status(order_status = order_status)

    def get_users_who_have_requested_a_refund(self):
        return self.get_queryset().get_users_who_have_requested_a_refund()

    def get_list_of_orders_per_user(self):
        return self.get_queryset().get_list_of_orders_per_user()

    def postal_address(self):
        """`Query`
            It will return the user adresses
        """
        return self.get_queryset().postal_address()

    def get_users_info(self):
        """returns user personal information"""
        return self.get_queryset().get_users_info()

    def get_users_with_the_most_voucher_consumption(self, limit_to:int=None):
        """
        get_users_with_the_most_voucher_consumption
        Get number with `number_of_voucher_used` attribute on Queryset
        PARAMS
        ------
        limit_to : int
            Indicates how many single used vouchers have been used by a user.
        """
        return self.get_queryset().get_users_with_the_most_voucher_consumption(limit_to)

    def income_of_each_account(self):
        """`Manager`
        caluculate the (quantity *(price - buy price))
        To achive the income of each user
        """
        return self.get_queryset().income_of_each_account()

    def user_address(self):
        """`Manager`
        we use this method to get the address for
        account/address
        """
        return self.get_queryset().user_address()

    def user_related(self):
        return self.get_queryset().user_related()