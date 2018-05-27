from django.conf import settings

SECONDS_IN_DAY = 60*60*24

DEFAULT_BACKEND = 'djmoney_rates.backends.OpenExchangeBackend'
EXCHANGE_URL = 'http://openexchangerates.org/api/latest.json'
EXCHANGE_BASE_CURRENCY = getattr(settings, 'DJANGO_MONEY_RATES', 'USD')
EXCHANGE_APP_ID = getattr(settings, 'EXCHANGE_APP_ID')
EXCHANGE_USE_CACHE = getattr(settings, 'EXCHANGE_USE_CACHE')
