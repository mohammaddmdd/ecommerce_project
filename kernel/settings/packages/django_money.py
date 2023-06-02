import moneyed
from django.utils.translation import gettext_lazy as _

RIAL = moneyed.add_currency(
    code='R',
    numeric='095',
    name=_('Iranian Rial'),
    countries=('Iran',)
)
TOMAN = moneyed.add_currency(
    code='T',
    numeric='095',
    name=_('Iranian Toman'),
    countries=('Iran',)
)
CURRENCIES = (
    'R',
    'T',
    'USD'
)
DEFAULT_CURRENCY_SHOW_ON_SITE = 'T'
USE_THOUSAND_SEPARATOR = True
