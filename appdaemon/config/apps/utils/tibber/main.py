from apps.utils.tibber.queries import TibberConsumerManager
from apps.utils.tibber.entities import Price, PriceInfo
from datetime import datetime

class Manager:
    
    def __init__(self):
        self.prices = PriceInfo()
    
    def update(self):
        supplier = TibberConsumerManager()
        response = supplier._get_prices_today()
        for item in response:
            self.prices.add(Price(starts_at=item.starts_at, price=item.total))
        return self.prices.prices
    

