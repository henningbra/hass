import unittest
from datetime import datetime, timedelta
from apps.utils.tibber.entities import Price, PriceInfo

delta = timedelta(days=1)
prices = [
    Price(starts_at=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)-delta, price=1.3),
    Price(starts_at=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0), price=1.3),
    Price(starts_at=datetime.now().replace(hour=1, minute=0, second=0, microsecond=0), price=2.0),
    Price(starts_at=datetime.now().replace(hour=2, minute=0, second=0, microsecond=0), price=0.0),
]

class TestPriceInfo(unittest.TestCase):

    def setUp(self):
        self.prices = PriceInfo(prices)

    def test_static_rounded_datetime(self):
        """ time rounded down to closest hour """
        datetime_sample = datetime.now().replace(minute=0, second=0, microsecond=0)
        rounded_datetime = PriceInfo.rounded_datetime(datetime.now())
        assert rounded_datetime == datetime_sample

    def test_static_now(self):
        """ Now rounded correctly """
        now_sample = datetime.now().replace(minute=0, second=0, microsecond=0)
        rounded_datetime = PriceInfo.now()
        assert rounded_datetime == now_sample

    def test_get_price_now(self):
        """ Get prices now """
        now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        price = self.prices.get_price(now)
        assert price.price == 1.3
    
    def test_unique_set(self):
        """ Check that hourly prices unique """ 
        self.prices.add(prices[0])
        assert len(self.prices.prices) == 4

    def test_get_prices(self):
        """ Getting low prices """
        prices = self.prices.get_prices(1)
        """ Check to see if only one returned """
        assert len(prices) == 1
        price = prices[0]
        """ Should return the lowest price """
        assert price.price == 0.0

    def test_get_prices_reverse(self):
        """ Getting high prices """
        prices = self.prices.get_prices(1, reverse=True)
        """ Check to see if only one returned """
        assert len(prices) == 1
        price = prices[0]
        """ Should return the higest price """
        assert price.price == 2.0

    def test_purge(self):
        """ Purge yesterday """
        self.prices.purge()
        """ Check to see if yesterday is purged """
        assert len(self.prices.prices) == 3

    def test_today_prices(self):
        """ Get todays prices """
        assert len(self.prices.get_today_prices()) == 3

    def test_price_now(self):
        assert len(self.prices.get_price_now(hours_low=1, hours_high=1)) == 1