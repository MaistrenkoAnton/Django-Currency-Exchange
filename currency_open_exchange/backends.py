import logging
import json

from django.core.exceptions import ImproperlyConfigured
from django.utils import six

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

from .exceptions import RateBackendError
from .models import Rate
from .settings import EXCHANGE_APP_ID, EXCHANGE_URL, EXCHANGE_BASE_CURRENCY

logger = logging.getLogger(__name__)


class RateBackend:
    source_name = "openexchange.org"

    def __init__(self):
        if not EXCHANGE_APP_ID:
            raise ImproperlyConfigured(
                "EXCHANGE_APP_ID setting should not be empty when using OpenExchangeBackend"
            )

        self.url = "{}?app_id={}&base={}".format(EXCHANGE_URL, EXCHANGE_APP_ID, EXCHANGE_BASE_CURRENCY)

    def update_rates(self):
        """
        Creates or updates rates for a source
        """
        rates = self.get_rates()
        for currency, value in six.iteritems(rates):
            try:
                rate = Rate.objects.get(currency=currency)
            except Rate.DoesNotExist:
                rate = Rate(currency=currency)

            rate.value = value
            rate.save()

    def get_rates(self):
        try:
            logger.debug("Connecting to url %s" % self.url)
            data = urlopen(self.url).read().decode("utf-8")
            return json.loads(data)['rates']

        except Exception as e:
            logger.exception("Error retrieving data from %s", self.url)
            raise RateBackendError("Error retrieving rates: %s" % e)
