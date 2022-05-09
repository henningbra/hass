from datetime import datetime

class Price:
    def __init__(self, starts_at: datetime, price: float):
        self.starts_at = starts_at
        self.price = price

    def __eq__(self, other):
        return self.starts_at == other.starts_at

    def __lt__(self, other):
        return self.starts_at < other.starts_at

    def __gt__(self, other):
        return self.starts_at > other.starts_at

    def __hash__(self):
        return hash(self.starts_at)

    def __str__(self):
        return f'Prices(starts_at={self.starts_at}, price={self.price}'

class PriceInfo:
    def __init__(self, prices=None):
        if prices is None:
            self.prices = set()
        else:
            self.prices = set(prices)

    def add(self, price: Price):
        return self.prices.add(price)

    @staticmethod
    def rounded_datetime(datetime: datetime):
        """ Returns datetime object rounded down to nearest hour"""
        return datetime.replace(minute=0, second=0, microsecond=0)

    @staticmethod
    def now(now=datetime.now()):
        """ Returns datetime object representing now rounded down to nearest hour"""
        return __class__.rounded_datetime(now)

    def get_price(self, datetime=datetime.now()):
        for price in self.prices:
            if price.starts_at == self.rounded_datetime(datetime):
                return price

    def get_prices(self, hours, reverse=False):
        sorted_list = sorted(self.prices, reverse=reverse, key=lambda prices: prices.price)
        return sorted_list[0:hours]
    
    def purge(self):
        for price in list(self.prices):
            if price.starts_at < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
                self.prices.remove(price)
        return self.prices

    def get_today_prices(self):
        start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end = datetime.now().replace(hour=23, minute=0, second=0, microsecond=0)
        prices = list(self.prices)
        today_prices = list()
        for price in prices:
            if price.starts_at >= start and price.starts_at <= end:
                today_prices.append(price)
        return today_prices

    def get_price_now(self, hours_low, hours_high):
        prices = self.get_today_prices()
        price = self.get_price()
        if price in self.get_today_prices(hours):
            price.level = 'LOW'
        if price in self.get_today_prices(hours=hours_low, reverse=True):
            price.level = 'HIGH'
        else:
            price.level = 'MEDIUM'
        return price


              

    