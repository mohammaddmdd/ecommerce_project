from django.test import TestCase
from collections import Counter
import random

from warehouse.repository.generator_layer import WarehouseDataGenerator
from basket.repository.generator_layer import BasketDataGenerator
from account.repository.generator_layer import AccountDataGenerator
from voucher.repository.generator_layer import VoucherDataGenerator
from logistic.repository.generator_layer import LogisticDataGenerator

from painless.utils.decorators import (
    disable_logging,
    test_time_upper_limit,
)

from account.models import User


class UserQuerysetManager(TestCase):
    TOTAL_PRODUCTS = 100

    @classmethod
    @disable_logging
    def setUpClass(cls) -> None:
        super(UserQuerysetManager, cls).setUpClass()

        # Account Data Generator
        account_dgl = AccountDataGenerator()
        account_dgl.create_user(10)
        account_dgl.create_profile()
        # Warehouse Data Generator
        warehouse_dgl = WarehouseDataGenerator()
        brands = warehouse_dgl.create_brands(5)
        categories = warehouse_dgl.create_categories(100)
        colors = warehouse_dgl.create_colors(10)
        warranties = warehouse_dgl.create_warranties(10)
        tags = warehouse_dgl.create_tags(5)
        products = warehouse_dgl.create_products(brands, categories, tags, 10)
        warehouse_dgl.create_physical_info()
        warehouse_dgl.create_packs(colors, warranties, products, 50)
        warehouse_dgl.create_expenses()
        warehouse_dgl.create_product_gallery(
            products,
            lower_boundary=3,
            upper_boundary=5
        )

        # Voucher Data Generator
        voucher_dgl = VoucherDataGenerator()
        vouchers = voucher_dgl.create_voucher(10)
        voucher_dgl.create_single_use_voucher()
        voucher_ranges = voucher_dgl.create_voucher_range()
        voucher_dgl.create_many_to_many_data(
            voucher_ranges=voucher_ranges,
            vouchers=vouchers,
        )

        # Logistic Data Generator
        logistic_dgl = LogisticDataGenerator()
        logistic_dgl.create_address(5)
        logistics = logistic_dgl.create_logistic(total=100)
        address = logistic_dgl.create_address()
        delivery_time_range = logistic_dgl.create_delivery_time_range(logistics=logistics, total=100 )
        logistic_distance_range = logistic_dgl.create_logistic_distance_range(logistics=logistics, total=100)
        logistic_weight_range = logistic_dgl.create_logistic_weight_range(logistics=logistics, total=100)
        logistic_cost_range = logistic_dgl.create_logistic_cost_range(logistics=logistics, total=100)

        # Basket Data Generator
        basket_dgl = BasketDataGenerator()
        basket_dgl.create_cart()
        basket_dgl.create_pack_cart()
        basket_dgl.create_order_addresses(10)
        orders = basket_dgl.create_orders()
        basket_dgl.create_pack_order(orders)
        basket_dgl.create_refund()

    @test_time_upper_limit(0.1)
    def test_queryset_get_list_of_orders_per_user(self):
        user_dal = User.dal.get_list_of_orders_per_user()
        actual = [user.orders_list for user in user_dal]
        users = User.objects.prefetch_related('orders').order_by('created')
        expected = [
            list(user.orders.all()) for user in users
        ]

        self.assertQuerysetEqual(
            actual,
            expected,
            msg=f"Actual list of orders per user is `{actual}` "
                f"but expected is `{expected}`.")

    def test_get_normal_users(self):
        users_dal = User.dal.get_normal_users()
        actual = users_dal

        users_obj = User.objects.all()
        expected = [
            users for users in users_obj
            if users.is_active 
            if not users.is_superuser 
            if not users.is_staff
            ]

        self.assertQuerysetEqual(actual,
                        expected,
                        ordered = False,
                        msg=f"Actual is `{actual}` "
                        f"but expected is `{expected}`")

    def test_get_actives(self):
        users_dal = User.dal.get_actives()
        actual = users_dal

        users_obj = User.objects.all()
        expected = [
            users for users in users_obj
            if users.is_active
            ]

        self.assertQuerysetEqual(actual,
                        expected,
                        ordered = False,
                        msg=f"Actual is `{actual}` "
                        f"but expected is `{expected}`")

    def test_get_users_who_made_the_most_number_of_purchases(self):
        users_dal = User.dal.get_users_who_made_the_most_number_of_purchases()
        users = users_dal
        actual = users.values_list('highest_number_of_purchases', flat=True)[:50]

        ids = [user.id for user in users_dal]
        users_obj = User.objects\
            .filter(id__in=ids)\
            .prefetch_related('orders__pack_orders')
        expected = [
            sum([
                pack_orders.quantity 
                for orders in user.orders.all() 
                for pack_orders in orders.pack_orders.all()
                ])
            for user in users_obj
            ]
    
        self.assertQuerysetEqual(
            actual,
            expected,
            ordered=False,
            msg=f"Actual purchases are `{actual}` "
            f"but expected is `{expected}`")

    def test_get_users_to_whom_we_have_sold_the_most(self):
        users_dal = User.dal.get_users_to_whom_we_have_sold_the_most()
        actual= [user.highest_amount_of_purchases for user in users_dal]

        ids = [user.id for user in users_dal]
        users_obj = User.objects\
            .filter(id__in=ids)\
            .prefetch_related('orders__pack_orders')
        user = [
            [
                pack_orders.quantity * pack_orders.cost.amount
                for orders in user.orders.all() 
                for pack_orders in orders.pack_orders.all()
                ]
            for user in users_obj
            ]
        expected = [sum(x) for x in user]

        self.assertEqual(
                    Counter(actual),
                    Counter(expected),
                    msg=f"Actual amount of purchase is `{actual}` "
                    f"but expected is `{expected}`")

    def test_get_users_from_whom_we_have_benefited_the_most(self):
        users_dal = User.dal.get_users_from_whom_we_have_benefited_the_most()
        actual= [user.highest_benefit for user in users_dal]

        ids = [user.id for user in users_dal]
        users_obj = User.objects\
            .filter(id__in=ids)\
            .prefetch_related('orders__pack_orders')
        user = [
            [
                pack_orders.quantity * (pack_orders.cost.amount - pack_orders.buy_price.amount)
                for orders in user.orders.all() 
                for pack_orders in orders.pack_orders.all()
                ]
            for user in users_obj
            ]
        expected = [sum(x) for x in user]

        self.assertEqual(
                    Counter(actual),
                    Counter(expected),
                    msg=f"Actual amount of benefit is `{actual}` "
                    f"but expected is `{expected}`")

    def test_get_users_who_bought_from_a_specific_brand(self):
        users_dal = User.dal\
            .get_users_who_bought_from_a_specific_brand(
                'BR-swelIfndgd30VbUlILtX0_umY5E'
                )
        expected = users_dal

        users_obj = User.objects\
            .prefetch_related(
                'orders__pack_orders__pack__product__brand'
                )
        actual = [
            user
            for user in users_obj                                 
            for orders in user.orders.all()
            for pack_orders in orders.pack_orders.all()
            if pack_orders.pack.product.brand.title in ('BR-swelIfndgd30VbUlILtX0_umY5E') 
            ]

        self.assertQuerysetEqual(
                    actual,
                    expected,
                    ordered=False,
                    msg=f"Actual is `{actual}` "
                    f"but expected is `{expected}`")

    def test_get_users_who_made_discounted_purchases(self):
        users_obj = User.dal.get_users_who_made_discounted_purchases()
        actual = users_obj

        users_obj = User.objects\
            .prefetch_related('orders__pack_orders__pack__product')
        expected = [
            user 
            for user in users_obj
            for orders in user.orders.all()
            for pack_orders in orders.pack_orders.all()
            if pack_orders.pack.product.is_voucher_active
        ]

        self.assertQuerysetEqual(
                    actual,
                    expected,
                    ordered=False,
                    msg=f"Actual is `{actual}` "
                    f"but expected is `{expected}`")

    def test_get_users_who_have_requested_a_refund(self):
        users_obj = User.dal.get_users_who_have_requested_a_refund()
        actual = users_obj

        users_obj = User.objects\
            .prefetch_related('orders__pack_orders')
        expected = [
            user
            for user in users_obj
            for orders in user.orders.all()
            for pack_orders in orders.pack_orders.all()
            if pack_orders.is_refunded
        ]

        self.assertQuerysetEqual(
                    actual,
                    expected,
                    ordered=False,
                    msg=f"Actual is `{actual}` "
                    f"but expected is `{expected}`")

    def test_get_amount_of_refund_request_per_user(self):
        users_obj = User.dal.get_amount_of_refund_request_per_user()
        actual = [user.refund_request_per_user for user in users_obj]

        users_obj = User.objects\
        .prefetch_related('orders__pack_orders')
        refund_list = [
            [1
            for orders in user.orders.all()
            for pack_orders in orders.pack_orders.all()
            if pack_orders.is_refunded]
            for user in users_obj
        ]
        expected = [len(refund) for refund in refund_list]

        self.assertQuerysetEqual(
                    actual,
                    expected,
                    ordered=False,
                    msg=f"Actual is `{actual}` "
                    f"but expected is `{expected}`")

    def test_get_users_who_have_made_several_purchases_of_a_certain_color(self):
        users_obj = User.dal.get_users_who_have_made_several_purchases_of_a_certain_color('Orange')
        actual = users_obj

        users_obj = User.objects\
            .prefetch_related(
                'orders__pack_orders__pack__color'
                )
        expected = [
            user
            for user in users_obj                                 
            for orders in user.orders.all()
            for pack_orders in orders.pack_orders.all()
            if pack_orders.pack.color.title == 'Orange'
            ]

        self.assertQuerysetEqual(
                    actual,
                    expected,
                    ordered=False,
                    msg=f"Actual is `{actual}` "
                    f"but expected is `{expected}`")

    def test_get_users_who_have_not_made_a_purchase_yet(self):
        users_dal = User.dal.get_users_who_have_not_made_a_purchase_yet()
        actual = users_dal

        users_obj = User.objects\
            .prefetch_related(
                'orders'
                )
        expected = [
            users
            for users in users_obj
            if users.orders is None
        ]

        self.assertQuerysetEqual(
                    actual,
                    expected,
                    ordered=False,
                    msg=f"Actual is `{actual}` "
                    f"but expected is `{expected}`")

    def test_get_total_delivered_or_canceled_order_per_user(self):
        users_dal = User.dal.get_total_delivered_or_canceled_order_per_user()
        actual = [user.cancelled_and_delivered for user in users_dal]
        
        users_obj = User.objects\
            .prefetch_related(
                'orders'
            )
        users = [
            [1
            for orders in user.orders.all()
            if orders.status == 'cancelled' or orders.status == 'delivered']
            for user in users_obj
        ]
        sum_orders = [sum(user) for user in users]
        expected=list(filter(None,sum_orders))

        self.assertQuerysetEqual(
                    actual,
                    expected,
                    ordered=False,
                    msg=f"Actual is `{actual}` "
                    f"but expected is `{expected}`")

    def test_get_order_status(self):
        status_list = ('waiting','expiring','cancelled','shipped','processing','delivered')
        status = random.choice(status_list)
        Users_dal = User.dal.get_order_status(status)
        actual = Users_dal

        user_obj = User.objects\
            .prefetch_related(
                'orders'
            )
        expected = [
            users
            for users in user_obj
            for orders in users.orders.all()
            if orders.status == status
        ]

        self.assertQuerysetEqual(
                    actual,
                    expected,
                    ordered=False,
                    msg=f"Actual is `{actual}` "
                    f"but expected is `{expected}`")