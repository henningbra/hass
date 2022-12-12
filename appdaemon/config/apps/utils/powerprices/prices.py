from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo


def map_fields(init_dict, map_dict, res_dict=None):
    # https://stackoverflow.com/questions/48203795/change-keys-of-a-dict-with-a-mapping-dict
    res_dict = res_dict or {}
    for k, v in init_dict.items():
        if isinstance(v, dict):
            v = map_fields(v, map_dict)
        if k in map_dict.keys():
            k = str(map_dict[k])
        res_dict[k] = v
    return res_dict


def map_list_of_dicts(lst: list, map_dict):
    result = list()
    for item in lst:
        result.append(map_fields(init_dict=item, map_dict=map_dict))
    return result


def get_power_price(date: datetime):
    # https://www.hvakosterstrommen.no/api/v1/prices/2022/12-12_NO2.json
    url = 'https://www.hvakosterstrommen.no/api/v1/prices'
    zone = 'N02'
    api=f'{url}/{date.year}/{date.month}-{date.day}_{zone}.json'
    result = requests.get(url)
    MAPPING = {'time_start': 'time', 'NOK_per_kWh': 'price'}
    return map_list_of_dicts(lst=result.json(), map_dict=MAPPING)


class Item:
    def __init__(self, time, price, *args, **kwargs):
        self.time = time if type(time) is datetime else datetime.fromisoformat(time)
        self.price = price
        self.rank = None

    def __str__(self):
        return str(self.time)

    def __hash__(self):
        return hash(self.time)

    def __eq__(self, other): 
        return self.time is other.time

    def __ne__(self, other): 
        return self.time is not other.time

    def __lt__(self, other): 
        return self.time < other.time


class Prices:
    
    def __init__(self):
        self.items = set()

    @property
    def today(self):
        return self._filter(delta_days=0)

    @property
    def tomorrow(self):
        return self._filter(delta_days=1)

    @staticmethod
    def _round(date):
        return date.replace(hour=0, minute=0, second=0, microsecond=0)

    @property
    def _now(self):
        return datetime.now().astimezone(tz=ZoneInfo(key='CET')).replace(hour=0, minute=0, second=0, microsecond=0)

    def _filter(self, delta_days=0):
        lst = list()
        for item in self.items:
            if self._now + timedelta(days=delta_days) <= item.time <= self._now.replace(hour=23) + timedelta(days=delta_days):
                lst.append(item)
        return sorted(lst, key=lambda x: x.price, reverse=False)

    def _set_ranks(self, prices):
        i = 0
        for price in prices:
            price.rank = i
            self.items.discard(price)
            self.items.add(price)
            i += 1
        
    def add(self, prices: list, *args, **kwargs):
        for price in prices:
            self.items.add(Item(**price))
        self._set_ranks(self.today)
        self._set_ranks(self.tomorrow)

    def fetch_today(self):
        result = get_power_price(datetime.now().astimezone(ZoneInfo(key='CET')))
        if result.status_code = 200
            self.add(result)

    def fetch_tomorrow(self):
        result = get_power_price(datetime.now().astimezone(ZoneInfo(key='CET')) + timedelta(days=1))
        if result.status_code = 200
            self.add(result)

    def __len__(self):
        return len(self.items)
            