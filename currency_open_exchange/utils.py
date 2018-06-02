import datetime
from decimal import Decimal
from .models import Rate

CURRENCIES = {}


def get_rate(currency):
    date = datetime.date.today()
    if currency in CURRENCIES and len(CURRENCIES[currency]) == 2 and CURRENCIES[currency][0] == date:
        return CURRENCIES[currency][1]

    rate = Rate.objects.filter(currency=currency).first()
    if not rate:
        return

    CURRENCIES[currency] = (date, rate.value)
    return rate.value


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
    rate = get_rate
    rate_from = rate(currency_from)
    rate_to = rate(currency_to)

    if not rate_from or not rate_to:
        return amount, currency_from

    new_amount = base_convert_money(amount, rate_from, rate_to)
    return new_amount, currency_to
