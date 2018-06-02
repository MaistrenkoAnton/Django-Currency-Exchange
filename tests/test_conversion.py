import datetime
from unittest import mock

from currency_open_exchange.models import Rate
from currency_open_exchange.utils import convert, get_rate, CURRENCIES
from decimal import Decimal
from django.test import SimpleTestCase


class ConversionTest(SimpleTestCase):

    def get_rate_mock(self, currency):
        if currency == 'USD':
            return self.usd_rate.value
        if currency == 'CNY':
            return self.cny_rate.value

    def setUp(self):
        self.usd_rate = mock.MagicMock(spec=Rate, value=1.000000, currency='USD')
        self.cny_rate = mock.MagicMock(spec=Rate, value=6.420400, currency='CNY')

    @mock.patch('currency_open_exchange.utils.get_rate')
    def test_convert_to_currency_ok(self, rate):
        expected_result = Decimal('64.20'), 'CNY'
        rate.side_effect = self.get_rate_mock
        result = convert(10, 'USD', 'CNY')

        self.assertEqual(result, expected_result)

    @mock.patch('currency_open_exchange.utils.get_rate')
    def test_convert_to_default_currency_ok(self, rate):
        expected_result = Decimal('15.58'), 'USD'
        rate.side_effect = self.get_rate_mock
        result = convert(100, 'CNY', 'USD')

        self.assertEqual(result, expected_result)

    @mock.patch('currency_open_exchange.utils.logger')
    @mock.patch('currency_open_exchange.utils.get_rate')
    def test_wrong_convert_from_currency(self, rate, logger):
        expected_result = Decimal('100'), 'WRONG'
        rate.side_effect = self.get_rate_mock
        result = convert(100, 'WRONG', 'USD')

        logger.error.assert_called_with('Cannot covert currency from WRONG to USD')
        self.assertEqual(result, expected_result)

    @mock.patch('currency_open_exchange.utils.logger')
    @mock.patch('currency_open_exchange.utils.get_rate')
    def test_wrong_convert_to_currency(self, rate, logger):
        expected_result = Decimal('100'), 'USD'
        rate.side_effect = self.get_rate_mock
        result = convert(100, 'USD', 'WRONG')

        logger.error.assert_called_with('Cannot covert currency from USD to WRONG')
        self.assertEqual(result, expected_result)

    @mock.patch('currency_open_exchange.utils.Rate')
    def test_get_rate_ok(self, rate):
        expected_result = 6.420400
        rate.objects.filter().first.return_value = self.cny_rate
        result = get_rate('CNY')

        self.assertEqual(result, expected_result)

    @mock.patch('currency_open_exchange.utils.CURRENCIES', {})
    @mock.patch('currency_open_exchange.utils.Rate')
    def test_get_rate_does_no_exist(self, rate):
        expected_result = None
        rate.objects.filter().first.return_value = None
        result = get_rate('WRONG')

        self.assertEqual(result, expected_result)

    @mock.patch('currency_open_exchange.utils.CURRENCIES', {'CNY': (str(datetime.date.today()), 6.420400)})
    @mock.patch('currency_open_exchange.utils.Rate')
    def test_get_rate_cached_ok(self, rate):
        expected_result = 6.420400
        result = get_rate('CNY')

        rate.objects.filter().first.assert_not_called()
        self.assertEqual(result, expected_result)

    @mock.patch('currency_open_exchange.utils.Rate')
    def test_get_rate_cache_updated_ok(self, rate):
        expected_result = {'CNY': (str(datetime.date.today()), 6.4204)}
        rate.objects.filter().first.return_value = self.cny_rate
        get_rate('CNY')

        self.assertEqual(CURRENCIES, expected_result)
