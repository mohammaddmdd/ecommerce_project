from decimal import Decimal

from djmoney.models.fields import MoneyField
from djmoney.money import Money
from djmoney.settings import DECIMAL_PLACES


class MoneyRialCurrencyOutput(MoneyField):

    def from_db_value(self, value, expression, connection):
        return Money(value, 'R')


class MoneyTomanCurrencyOutput(MoneyField):

    def from_db_value(self, value, expression, connection):
        return Money(value, 'T')


class MoneyDollarCurrencyOutput(MoneyField):

    def from_db_value(self, value, expression, connection):
        return Money(value, 'USD')


class MoneyCurrencyOutput(MoneyField):
    def __init__(self, currency, *args, **kwargs):
        self.currency = currency

        if kwargs.get('decimal_places'):
            self.decimal_places = kwargs.get('decimal_places')
        else:
            self.decimal_places = DECIMAL_PLACES

        super().__init__(currency, *args, **kwargs)

    def from_db_value(self, value, expression, connection):
        value = round(Decimal(value), 2)
        money = Money(
            value,
            self.currency
        )

        return money
