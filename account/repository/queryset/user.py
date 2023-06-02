from django.db.models import QuerySet
from django.apps import apps

from django.db.models import (
    QuerySet,
    Count,
    Sum,
    F,
    Q,
    Prefetch,
    DecimalField,
)

from django.db.models.functions import Coalesce


class UserQuerySet(QuerySet):
    def get_normal_users(self):
        """get normal users"""
        qs = self.filter(
            Q(is_superuser=False) &
            Q(is_staff=False) &
            Q(is_active=True)
        )
        return qs

    def get_actives(self, is_active=True):
        """Get all active/inactive users"""
        qs = self.filter(is_active=is_active)
        return qs

    def get_users_who_made_the_most_number_of_purchases(self):
        """
        The users who made the most number of purchases 
        sorted by descending order
        -----
        Get highest number of purchases with `highest_number_of_purchases` attribute on Queryset
        """
        qs = self.prefetch_related('orders__pack_orders') \
            .annotate(
            highest_number_of_purchases=Coalesce
            (Sum('orders__pack_orders__quantity'), 0)) \
            .order_by('-highest_number_of_purchases'
                      )
        return qs

    def get_users_to_whom_we_have_sold_the_most(self):
        """
        return's The users to whom we have sold the most
        sorted by descending order
        -----
        Get users we have sold the most
        with `highest_amount_of_purchases` attribute on Queryset
        """
        qs = self.prefetch_related('orders__pack_orders') \
            .annotate(highest_amount_of_purchases=Coalesce(
            Sum(F('orders__pack_orders__quantity') *
                F('orders__pack_orders__cost')), 0, output_field=DecimalField()
        )) \
            .order_by('-highest_amount_of_purchases'
                      )
        return qs

    def get_users_from_whom_we_have_benefited_the_most(self):
        """
        return's users from whom we have benefited the most
        sorted by descending order
        -----
        Get users from whom we have benefited the most
        with `highest_benefit` attribute on Queryset
        """
        qs = self.prefetch_related('orders__pack_orders') \
            .annotate(highest_benefit=Coalesce(
            Sum(F('orders__pack_orders__quantity') * (
                    F('orders__pack_orders__cost') -
                    F('orders__pack_orders__buy_price'))), 0, output_field=DecimalField()
        )) \
            .order_by('-highest_benefit')
        return qs

    def get_users_who_bought_from_a_specific_brand(self, brand_title: str):
        """
        return's List of users who bought from a specific brand
        """
        qs = self.prefetch_related(
            'orders__pack_orders__pack__product__brand') \
            .filter(orders__pack_orders__pack__product__brand__title__iexact=brand_title)
        return qs

    def get_users_who_made_discounted_purchases(self):
        """
        return's List of users who made discounted purchases
        """
        qs = self.prefetch_related(
            'orders__pack_orders__pack__product') \
            .filter(
            Q(orders__isnull=False) &
            Q(orders__pack_orders__pack__product__is_voucher_active=True))
        return qs

    def get_users_who_have_not_made_a_purchase_yet(self):
        """
        return's list of users who have not made a purchase yet
        """
        qs = self.prefetch_related('orders') \
            .filter(orders__isnull=True)
        return qs

    def get_users_who_have_requested_a_refund(self):
        """
        return's list of users who have requested a refund
        """
        qs = self.prefetch_related('orders__pack_orders') \
            .filter(orders__pack_orders__is_refunded=True)
        return qs

    def get_amount_of_refund_request_per_user(self):
        """
        return's Amount of refund request per user
        -----
        Get amount of refund request per user
        with `refund_request_per_user` attribute on Queryset
        """
        qs = self.prefetch_related('orders__pack_orders') \
            .annotate(refund_request_per_user=
                      Count('orders__pack_orders',
                            filter=Q(orders__pack_orders__is_refunded=True)))
        return qs

    def get_users_who_have_made_several_purchases_of_a_certain_color(self, color_title: str):
        """
        return's list of users who have made several purchases of a certain color
        """
        qs = self.prefetch_related('orders__pack_orders__pack__color') \
            .filter(orders__pack_orders__pack__color__title__iexact=color_title)
        return qs

    def get_total_delivered_or_canceled_order_per_user(self):
        """
        Total delivered or canceled orders for each user
        -----
        Get total delivered or canceled orders for each user
        with `cancelled_and_delivered` attribute on Queryset
        """
        qs = self.filter(
            Q(orders__status='cancelled') |
            Q(orders__status='delivered')) \
            .annotate(cancelled_and_delivered=Coalesce(Count('orders__status'), 0))
        return qs

    def get_order_status(self, order_status: str):
        """
        get's user order status

        PARAM
        ------
        'order_status' : str
            you can get users' order status by params given below:
            'waiting'
            'expiring'
            'cancelled'
            'shipped'
            'processing'
            'delivered'
        """
        qs = self.prefetch_related('orders') \
            .filter(orders__status=order_status)
        return qs

    def get_list_of_orders_per_user(self):
        Order = apps.get_model('basket', 'order')
        return self.prefetch_related(
            Prefetch('orders',
                     queryset=Order.objects.order_by('created'),
                     to_attr='orders_list')
        )

    def postal_address(self):
        """`Query`
            It will return the user adresses
        """
        return self \
            .annotate(
            postal_ad=F("addresses__postal_address")) \
            .values("postal_ad")

    def get_users_info(self):
        """returns user personal information
        -----
        Get user gender by `user_gender`
        and user birthdate by `user_birthdate`
        
        """
        return self.annotate(
            user_gender=F("profile__gender"),
            user_birth_date=F("profile__birth_date"))

    def get_users_with_the_most_voucher_consumption(self, limit_to: int = None):
        """
        get_users_with_the_most_voucher_consumption
        Get number with `number_of_voucher_used` attribute on Queryset
        PARAMS
        ------
        limit_to : int
            Indicates how many single used vouchers have been used by a user.
        """
        qs = self.prefetch_related('orders') \
            .annotate(number_of_voucher_used=Count('orders__vouchers',
                                                   filter=Q(orders__vouchers__isnull=False))) \
            .order_by('-number_of_voucher_used')
        if limit_to is not None:
            qs = qs[:limit_to]
        return qs

    def income_of_each_account(self):
        """`Queryset`
        caluculate the (quantity *(price - buy price))
        To achive the income of each user
        """
        return self.annotate(
            user_income=
            (
                    F("cart__pack_carts__quantity")
                    * (F("cart__pack_carts__pack__expense__price")
                       - F("cart__pack_carts__pack__expense__buy_price")))) \
            .values("user_income")

    def user_address(self):
        """
        `Querset`
        we use this method to get the address for
        account/address
        """
        return self.annotate(user_addres=F("addresses"))

    def user_related(self):
        return self.prefetch_related('addresses')
