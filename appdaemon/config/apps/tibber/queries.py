from sgqlc.endpoint.http import HTTPEndpoint
from sgqlc.operation import Operation
from schema import Query, Price
import settings
import time

endpoint = HTTPEndpoint(settings.TIBBER_URL, settings.TIBBER_HEADERS)


def query_today_prices() -> list(Price):

    op = Operation(Query)
    viewer = op.viewer()
    homes = viewer.homes
    subscription = homes.current_subscription
    today = subscription.price_info.today
    today.__fields__('total', 'starts_at')

    json_data = endpoint(op)
    obj = op + json_data
    return obj.viewer.homes[0].current_subscription.price_info.today


if __name__ == "__main__":
    prices = query_today_prices()
    print(prices)