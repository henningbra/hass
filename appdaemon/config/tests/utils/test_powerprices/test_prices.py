import unittest
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from apps.utils.powerprices.prices import map_fields, map_list_of_dicts, Item, Prices

# https://www.hvakosterstrommen.no/strompris-api

NOW = datetime.now().astimezone(ZoneInfo(key='CET')).replace(minute=0, second=0, microsecond=0)
TODAY = NOW.replace(hour=0)
TOMORROW = TODAY + timedelta(days=1)

def MOCK_FACTORY(delta_days=0):
    lst = list()
    for hour in range(24):
        item = dict()
        item['NOK_per_kWh'] = hour
        time = NOW.replace(hour=hour) + timedelta(days=delta_days)
        item['time_start'] = time.isoformat()
        lst.append(item)
    return lst

MOCK_PRICES = MOCK_FACTORY()
MAPPING = {'time_start': 'time', 'NOK_per_kWh': 'price'}
MAPPED_MOCK_TODAY=map_list_of_dicts(lst=MOCK_FACTORY(delta_days=0), map_dict=MAPPING)
MAPPED_MOCK_TOMORROW=map_list_of_dicts(lst=MOCK_FACTORY(delta_days=1), map_dict=MAPPING)

# response = requests.get('https://www.hvakosterstrommen.no/api/v1/prices/2022/12-12_NO2.json')
# MOCK_PRICES = response.json()
# MAPPING = {'time_start': 'time', 'NOK_per_kWh': 'price'}
# MAPPED_MOCK_TODAY=map_list_of_dicts(MOCK_PRICES, map_dict=MAPPING)
# MAPPED_MOCK_TOMORROW=map_list_of_dicts(lst=MOCK_FACTORY(delta_days=1), map_dict=MAPPING)

class Testmapping(unittest.TestCase):

    def test_map_fields(self):
        dct =  map_fields(init_dict=MOCK_PRICES[0], map_dict=MAPPING)
        assert 'time' in dct.keys()
        assert 'price' in dct.keys()

    def test_map_list_of_dicts(self):
        lst =  map_list_of_dicts(lst=MOCK_PRICES, map_dict=MAPPING)
        assert 'time' in lst[0].keys()
        assert 'price' in lst[0].keys()

    def test_map_list_of_dicts_is_today(self):
        lst =  MAPPED_MOCK_TODAY
        assert datetime.fromisoformat(lst[0]['time']) == TODAY

    def test_map_list_of_dicts_is_tomorrow(self):
        lst =  MAPPED_MOCK_TOMORROW
        assert datetime.fromisoformat(lst[0]['time']) == TOMORROW


class TestItem(unittest.TestCase):

    def setUp(self):
        time = datetime.fromisoformat('2022-12-08T00:00:00+01:00')
        price = 3.08755
        self.item = Item(time=time, price=price)
    
    def test_item(self):
        assert type(self.item.time) is datetime
        assert type(self.item.price) is float
        assert hash(self.item)


class TestPrices(unittest.TestCase):

    def setUp(self):
        self.prices = Prices()
    
    def test_prices(self):
        assert len(self.prices) == 0
    
    def test_now(self):
        assert self.prices._now == TODAY


class TestPricesItems(unittest.TestCase):

    def setUp(self):
        self.prices = Prices()
        self.prices.add(MAPPED_MOCK_TODAY)
        self.prices.add(MAPPED_MOCK_TOMORROW)

    def test_prices(self):
        assert len(self.prices) == 48

    def test_prices(self):
        assert len(self.prices.items) == 48

    def test_prices_items(self):
        assert len(self.prices) == len(self.prices.items)

    def test_today(self):
        assert len(self.prices.today) == 24
        assert self.prices.today[0].time == TODAY

    def test_tomorrow(self):
        assert len(self.prices.tomorrow) == 24
        assert self.prices.tomorrow[0].time == TOMORROW

    def test_rank(self):
        assert self.prices.today[0].rank == 0
        assert self.prices.today[0].time == TODAY
        assert self.prices.today[23].rank == 23
        assert self.prices.today[23].time == TODAY.replace(hour=23)
        assert self.prices.tomorrow[0].rank == 0
        assert self.prices.tomorrow[0].time == TOMORROW
        assert self.prices.tomorrow[23].rank == 23
        assert self.prices.tomorrow[23].time == TOMORROW.replace(hour=23)

    def test_TODO(self):
        # decouple timezone
        # put input into right timezone
        assert True
