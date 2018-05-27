from decimal import Decimal
from django.core.cache import cache

from .settings import EXCHANGE_USE_CACHE, SECONDS_IN_DAY
from .models import Rate


def get_rate_from_cache(currency):
    """Returns the rate from the default currency to `currency`."""
    value = cache.get(currency)
    if not value:
        rate = get_rate(currency)
        if EXCHANGE_USE_CACHE and rate:
            cache.set(currency, rate, SECONDS_IN_DAY)
    return value


def get_rate(currency):
    rate = Rate.objects.filter(currency=currency).first()
    return rate.value if rate else None


def base_convert_money(amount, rate_from, rate_to):
    """
    Convert 'amount' from 'currency_from' to 'currency_to'
    """
    return ((get_decimal(amount) / get_decimal(rate_from)) * get_decimal(rate_to)).quantize(Decimal("1.00"))


def get_decimal(value):
    return Decimal(value).quantize(Decimal('.000001'))


def convert(amount, currency_from, currency_to):
    """
    Convert 'amount' from 'currency_from' to 'currency_to' and return a Money
    instance of the converted amount.
    """
    rate = get_rate_from_cache if EXCHANGE_USE_CACHE else get_rate
    rate_from = rate(currency_from)
    rate_to = rate(currency_to)

    if not rate_from or not rate_to:
        return amount, currency_from

    new_amount = base_convert_money(amount, rate_from, rate_to)
    return new_amount, currency_to
