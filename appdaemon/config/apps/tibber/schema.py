from sgqlc.types import Type, Field, list_of, Enum, ID, String, Float
from sgqlc.types.datetime import DateTime
from sgqlc.operation import Operation


# https://developer.tibber.com/docs/reference#pricelevel
class PriceLevel(Enum):
    __choices__ = ('NORMAL', 'CHEAP', 'VERY_CHEAP', 'EXPENSIVE', 'VERY_EXPENSIVE')


# https://developer.tibber.com/docs/reference#price
class Price(Type):
    total = Float
    energy = Float
    tax = Float
    starts_at = DateTime
    currency = String
    level = PriceLevel


# https://developer.tibber.com/docs/reference#priceinfo
class PriceInfo(Type):
    current = Field(Price)
    today = list_of(Price)
    tomorrow = list_of(Price)


# https://developer.tibber.com/docs/reference#subscription
class Subscription(Type):
    price_info = Field(PriceInfo)


# https://developer.tibber.com/docs/reference#home
class Home(Type):
    id = ID
    current_subscription = Field(Subscription)


# https://developer.tibber.com/docs/reference#viewer
class Viewer(Type):
    homes = list_of(Home)
    home = Field(Home)


class Query(Type):  # GraphQL's root
    viewer = Field(Viewer)


if __name__ == "__main__":
    op = Operation(Query)
    viewer = op.viewer()
    # viewer.homes.current_subscription.price_info.today.__fields__('total', 'starts_at', 'level')
    print(op)
    