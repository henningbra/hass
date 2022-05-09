import os
from sgqlc.endpoint.http import HTTPEndpoint
from sgqlc.operation import Operation
from apps.utils.tibber.schema import Query


TIBBER_URL = os.getenv('TIBBER_URL', default='https://api.tibber.com/v1-beta/gql')
TIBBER_TOKEN = os.getenv('TIBBER_TOKEN', default='your_secret_tibber_token_here')
TIBBER_HEADERS = {
    'Authorization': f'Bearer {TIBBER_TOKEN}',
    'Content-Type': 'application/json'
}

endpoint = HTTPEndpoint(TIBBER_URL, TIBBER_HEADERS)


class TibberConsumerManager:

    def __init__(self):
        self.operation = Operation(Query)
        self.viewer = self.operation.viewer()
        self.homes = self.viewer.homes
        self.subscription = self.homes.current_subscription

    def _get_prices_today(self):
        today = self.subscription.price_info.today
        today.__fields__('total', 'starts_at')
        json_data = endpoint(self.operation)
        obj = self.operation + json_data
        return obj.viewer.homes[0].current_subscription.price_info.today

    def _get_prices_tomorrow(self):
        tomorrow = self.subscription.price_info.tomorrow
        tomorrow.__fields__('total', 'starts_at')
        json_data = endpoint(self.operation)
        obj = self.operation + json_data
        return obj.viewer.homes[0].current_subscription.price_info.tomorrow
